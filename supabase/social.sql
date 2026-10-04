-- Flag Dash: friends and inbox.
-- Run this once in Supabase: SQL Editor -> New query -> paste everything -> Run.
-- Safe to run again. Needs accounts.sql to have been run first.
--
-- fd_people   one public card per signed-in player: friend code, name, flag, last seen.
-- fd_friends  friend list and friend requests.
-- fd_inbox    messages that wait for the player, even when they are offline.
-- fd_blocks   players someone has blocked (their messages and requests are dropped).
-- Everything is changed through the fd_* functions below, which check who is calling.

create table if not exists public.fd_people (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  code         text not null unique check (code ~ '^[A-Z2-9]{6}$'),
  nm           text not null default 'Runner' check (char_length(nm) between 1 and 24),
  cc           text not null default 'USA' check (cc ~ '^[A-Z]{3}$'),
  friends_only boolean not null default false,
  seen         timestamptz not null default now()
);

create table if not exists public.fd_friends (
  user_id   uuid not null references auth.users(id) on delete cascade,
  friend_id uuid not null references auth.users(id) on delete cascade,
  status    text not null check (status in ('sent','friend')),
  created   timestamptz not null default now(),
  primary key (user_id, friend_id),
  check (user_id <> friend_id)
);
create index if not exists fd_friends_to on public.fd_friends(friend_id);

create table if not exists public.fd_inbox (
  id      bigserial primary key,
  to_id   uuid not null references auth.users(id) on delete cascade,
  from_id uuid references auth.users(id) on delete set null,
  from_nm text not null,
  from_cc text not null,
  kind    text not null check (kind in ('msg','invite','gift')),
  body    text not null default '' check (char_length(body) <= 300),
  room    text check (room ~ '^[A-Z]{4}$'),
  created timestamptz not null default now(),
  read    boolean not null default false
);
-- gifts were added later: make sure tables made by an older version of this script allow them
alter table public.fd_inbox drop constraint if exists fd_inbox_kind_check;
alter table public.fd_inbox add constraint fd_inbox_kind_check check (kind in ('msg','invite','gift'));
create index if not exists fd_inbox_to on public.fd_inbox(to_id, created desc);
create index if not exists fd_inbox_from on public.fd_inbox(from_id, created desc);

create table if not exists public.fd_blocks (
  user_id    uuid not null references auth.users(id) on delete cascade,
  blocked_id uuid not null references auth.users(id) on delete cascade,
  primary key (user_id, blocked_id)
);

alter table public.fd_people  enable row level security;
alter table public.fd_friends enable row level security;
alter table public.fd_inbox   enable row level security;
alter table public.fd_blocks  enable row level security;
revoke all on public.fd_people, public.fd_friends, public.fd_inbox, public.fd_blocks from anon, authenticated;
grant select on public.fd_inbox to authenticated;
grant update (read) on public.fd_inbox to authenticated;
grant delete on public.fd_inbox to authenticated;

drop policy if exists "read my inbox"   on public.fd_inbox;
drop policy if exists "mark my inbox"   on public.fd_inbox;
drop policy if exists "delete my inbox" on public.fd_inbox;
create policy "read my inbox"   on public.fd_inbox for select to authenticated using (to_id = auth.uid());
create policy "mark my inbox"   on public.fd_inbox for update to authenticated using (to_id = auth.uid()) with check (to_id = auth.uid());
create policy "delete my inbox" on public.fd_inbox for delete to authenticated using (to_id = auth.uid());

-- Create or refresh my card. Returns my friend code.
create or replace function public.fd_me(p_nm text, p_cc text, p_friends_only boolean default false)
returns text language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); c text; v_nm text; v_cc text;
begin
  if me is null then return null; end if;
  v_nm := left(nullif(btrim(regexp_replace(coalesce(p_nm,''), '[[:cntrl:]]', '', 'g')), ''), 24);
  v_cc := case when p_cc ~ '^[A-Z]{3}$' then p_cc else 'USA' end;
  select code into c from fd_people where user_id = me;
  if c is null then
    loop
      c := (select string_agg(substr('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', 1 + floor(random()*32)::int, 1), '') from generate_series(1,6));
      begin
        insert into fd_people(user_id, code, nm, cc, friends_only) values (me, c, coalesce(v_nm,'Runner'), v_cc, coalesce(p_friends_only,false));
        exit;
      exception when unique_violation then
        if exists (select 1 from fd_people where user_id = me) then select code into c from fd_people where user_id = me; exit; end if;
      end;
    end loop;
  else
    update fd_people set nm = coalesce(v_nm, fd_people.nm), cc = v_cc, friends_only = coalesce(p_friends_only,false), seen = now() where user_id = me;
  end if;
  return c;
end $$;

-- Look a player up by friend code (to add them).
create or replace function public.fd_find(p_code text)
returns table(uid uuid, nm text, cc text) language sql stable security definer set search_path = public as $$
  select user_id, nm, cc from fd_people where code = upper(btrim(p_code)) and auth.uid() is not null;
$$;

-- My friends, requests I sent, and requests waiting for me.
-- kind: 'friend', 'sent' (waiting for them), 'incoming' (waiting for me)
create or replace function public.fd_friend_list()
returns table(uid uuid, nm text, cc text, code text, kind text, seen timestamptz)
language sql stable security definer set search_path = public as $$
  select p.user_id, p.nm, p.cc, p.code, case when f.status = 'friend' then 'friend' else 'sent' end, p.seen
    from fd_friends f join fd_people p on p.user_id = f.friend_id
   where f.user_id = auth.uid()
  union all
  select p.user_id, p.nm, p.cc, p.code, 'incoming', p.seen
    from fd_friends f join fd_people p on p.user_id = f.user_id
   where f.friend_id = auth.uid() and f.status = 'sent'
     and not exists (select 1 from fd_friends r where r.user_id = auth.uid() and r.friend_id = f.user_id);
$$;

-- Send a friend request (or accept theirs if they already asked me).
create or replace function public.fd_friend_add(p_to uuid)
returns text language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if me is null then return 'signed out'; end if;
  if p_to is null or p_to = me or not exists (select 1 from fd_people where user_id = p_to) then return 'not found'; end if;
  if not exists (select 1 from fd_people where user_id = me) then return 'no card'; end if;
  if exists (select 1 from fd_blocks where user_id = p_to and blocked_id = me) then return 'sent'; end if;
  if exists (select 1 from fd_friends where user_id = me and friend_id = p_to) then
    return (select case when status = 'friend' then 'friends' else 'sent' end from fd_friends where user_id = me and friend_id = p_to);
  end if;
  if (select count(*) from fd_friends where user_id = me) >= 200 then return 'full'; end if;
  if (select count(*) from fd_friends where user_id = me and status = 'sent' and created > now() - interval '1 hour') >= 30 then return 'slow'; end if;
  if exists (select 1 from fd_friends where user_id = p_to and friend_id = me) then
    update fd_friends set status = 'friend' where user_id = p_to and friend_id = me;
    insert into fd_friends(user_id, friend_id, status) values (me, p_to, 'friend');
    return 'friends';
  end if;
  insert into fd_friends(user_id, friend_id, status) values (me, p_to, 'sent');
  return 'sent';
end $$;

-- Answer a friend request.
create or replace function public.fd_friend_answer(p_from uuid, p_yes boolean)
returns text language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if me is null then return 'signed out'; end if;
  if not exists (select 1 from fd_friends where user_id = p_from and friend_id = me) then return 'not found'; end if;
  if p_yes then
    update fd_friends set status = 'friend' where user_id = p_from and friend_id = me;
    insert into fd_friends(user_id, friend_id, status) values (me, p_from, 'friend')
      on conflict (user_id, friend_id) do update set status = 'friend';
    return 'friends';
  end if;
  delete from fd_friends where user_id = p_from and friend_id = me;
  return 'declined';
end $$;

-- Remove a friend, or cancel a request, in both directions.
create or replace function public.fd_friend_remove(p_other uuid)
returns text language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then return 'signed out'; end if;
  delete from fd_friends where (user_id = auth.uid() and friend_id = p_other) or (user_id = p_other and friend_id = auth.uid());
  return 'removed';
end $$;

-- Block or unblock a player. Blocking also removes them as a friend.
create or replace function public.fd_block(p_other uuid, p_on boolean)
returns text language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null or p_other is null or p_other = auth.uid() then return 'no'; end if;
  if p_on then
    insert into fd_blocks values (auth.uid(), p_other) on conflict do nothing;
    delete from fd_friends where (user_id = auth.uid() and friend_id = p_other) or (user_id = p_other and friend_id = auth.uid());
    delete from fd_inbox where to_id = auth.uid() and from_id = p_other;
  else
    delete from fd_blocks where user_id = auth.uid() and blocked_id = p_other;
  end if;
  return 'ok';
end $$;

-- Send an inbox message, race invite or gift (the gift's item id goes in the body).
-- Limits: 300 characters, 5 per minute, 60 per hour.
create or replace function public.fd_send(p_to uuid, p_kind text, p_body text, p_room text default null)
returns text language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); card fd_people; them fd_people; b text;
begin
  if me is null then return 'signed out'; end if;
  select * into card from fd_people where user_id = me;
  if not found then return 'no card'; end if;
  if p_to is null or p_to = me then return 'not found'; end if;
  select * into them from fd_people where user_id = p_to;
  if not found then return 'not found'; end if;
  if p_kind not in ('msg','invite','gift') then return 'bad kind'; end if;
  b := left(btrim(regexp_replace(coalesce(p_body,''), '[[:cntrl:]]', ' ', 'g')), 300);
  if p_kind = 'msg' and b = '' then return 'empty'; end if;
  if p_kind = 'invite' and (p_room is null or p_room !~ '^[A-Z]{4}$') then return 'bad room'; end if;
  if p_kind = 'gift' and b !~ '^g_[a-z]{2,20}$' then return 'bad gift'; end if;
  if (select count(*) from fd_inbox where from_id = me and created > now() - interval '1 minute') >= 5
     or (select count(*) from fd_inbox where from_id = me and created > now() - interval '1 hour') >= 60 then return 'slow'; end if;
  -- blocked, or they only take messages from friends: pretend it was sent
  if exists (select 1 from fd_blocks where user_id = p_to and blocked_id = me) then return 'sent'; end if;
  if them.friends_only and not exists (select 1 from fd_friends where user_id = p_to and friend_id = me and status = 'friend') then return 'friends only'; end if;
  insert into fd_inbox(to_id, from_id, from_nm, from_cc, kind, body, room)
    values (p_to, me, card.nm, card.cc, p_kind, b, case when p_kind = 'invite' then p_room end);
  update fd_people set seen = now() where user_id = me;
  -- keep each inbox to the newest 100 messages, and nothing older than 60 days
  delete from fd_inbox where to_id = p_to and (created < now() - interval '60 days'
    or id not in (select id from fd_inbox where to_id = p_to order by created desc limit 100));
  return 'sent';
end $$;

revoke all on function public.fd_me(text,text,boolean), public.fd_find(text), public.fd_friend_list(), public.fd_friend_add(uuid),
  public.fd_friend_answer(uuid,boolean), public.fd_friend_remove(uuid), public.fd_block(uuid,boolean), public.fd_send(uuid,text,text,text) from public, anon;
grant execute on function public.fd_me(text,text,boolean), public.fd_find(text), public.fd_friend_list(), public.fd_friend_add(uuid),
  public.fd_friend_answer(uuid,boolean), public.fd_friend_remove(uuid), public.fd_block(uuid,boolean), public.fd_send(uuid,text,text,text) to authenticated;
