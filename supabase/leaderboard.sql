-- Race Your Flag: worldwide leaderboard.
-- Run this once in Supabase: SQL Editor -> New query -> paste everything -> Run.
-- It is safe to run again; it only creates what is missing and replaces the functions.

-- One row per player. The secret proves a save comes from that player's device; nobody can read it.
create table if not exists public.fd_players (
  pid         text primary key check (pid ~ '^p[a-z0-9]{8,16}$'),
  secret_hash text not null,
  last_submit timestamptz not null default now()
);

-- One row per player per leaderboard period (d = day, w = week, s = season, a = all-time).
create table if not exists public.fd_scores (
  pid        text not null references public.fd_players(pid) on delete cascade,
  period     text not null check (period in ('d','w','s','a')),
  pkey       text not null check (pkey ~ '^[0-9A-Za-z-]{2,12}$'),
  nm         text not null default 'Runner',
  cc         text not null default 'USA',
  gid        text, gt text, gn text, gc text,
  pts        int  not null default 0,
  races      int  not null default 0,
  gb         int  not null default 0,
  updated_at timestamptz not null default now(),
  primary key (pid, period, pkey)
);
-- profile picture: which hero and skin to draw (added later, so older tables get the column too)
alter table public.fd_scores add column if not exists av text check (av is null or av ~ '^[a-z]{2,12}\.[a-z0-9_]{2,24}$');
create index if not exists fd_scores_board on public.fd_scores (period, pkey, pts desc);

-- Anyone may read the boards. Nobody may write to the tables directly: saves go through fd_submit.
alter table public.fd_players enable row level security;
alter table public.fd_scores  enable row level security;
drop policy if exists "boards are public" on public.fd_scores;
create policy "boards are public" on public.fd_scores for select to anon, authenticated using (true);
revoke all on public.fd_players from anon, authenticated;
revoke all on public.fd_scores  from anon, authenticated;
grant select on public.fd_scores to anon, authenticated;

-- Save a player's points. Points only go up, and by a limited amount per save,
-- and a device can save at most once every 20 seconds.
create or replace function public.fd_submit(p_pid text, p_secret text, p_card jsonb)
returns text language plpgsql security definer set search_path = public as $$
declare
  pl  public.fd_players;
  r   jsonb;
  old public.fd_scores;
  h   text;
  np int; nr int; ngb int;
begin
  if p_pid !~ '^p[a-z0-9]{8,16}$' or length(coalesce(p_secret,'')) not between 16 and 64 then return 'bad'; end if;
  h := encode(sha256(convert_to(p_secret, 'UTF8')), 'hex');
  select * into pl from public.fd_players where pid = p_pid;
  if not found then
    insert into public.fd_players(pid, secret_hash, last_submit) values (p_pid, h, now() - interval '1 hour');
    select * into pl from public.fd_players where pid = p_pid;
  elsif pl.secret_hash <> h then
    return 'denied';
  end if;
  if pl.last_submit > now() - interval '20 seconds' then return 'slow'; end if;
  update public.fd_players set last_submit = now() where pid = p_pid;

  for r in select * from jsonb_array_elements(coalesce(p_card->'rows', '[]'::jsonb)) loop
    continue when coalesce(r->>'p','') not in ('d','w','s','a') or coalesce(r->>'k','') !~ '^[0-9A-Za-z-]{2,12}$';
    old := null;
    select * into old from public.fd_scores where pid = p_pid and period = r->>'p' and pkey = r->>'k';
    np  := least(greatest(coalesce((r->>'pts')::int, 0), coalesce(old.pts, 0)),   coalesce(old.pts, 0) + 120);
    nr  := least(greatest(coalesce((r->>'r')::int, 0),   coalesce(old.races, 0)), coalesce(old.races, 0) + 6);
    ngb := least(greatest(coalesce((r->>'gb')::int, 0),  coalesce(old.gb, 0)),    coalesce(old.gb, 0) + 30);
    insert into public.fd_scores(pid, period, pkey, nm, cc, av, gid, gt, gn, gc, pts, races, gb, updated_at)
    values (p_pid, r->>'p', r->>'k',
            left(coalesce(nullif(p_card->>'nm',''), 'Runner'), 16),
            case when coalesce(p_card->>'cc','') ~ '^[A-Z]{3}$' then p_card->>'cc' else 'USA' end,
            case when coalesce(p_card->>'av','') ~ '^[a-z]{2,12}\.[a-z0-9_]{2,24}$' then p_card->>'av' end,
            left(p_card->>'gid', 16), left(p_card->>'gt', 4), left(p_card->>'gn', 20), left(p_card->>'gc', 7),
            np, nr, ngb, now())
    on conflict (pid, period, pkey) do update
      set nm = excluded.nm, cc = excluded.cc, av = excluded.av, gid = excluded.gid, gt = excluded.gt, gn = excluded.gn, gc = excluded.gc,
          pts = excluded.pts, races = excluded.races, gb = excluded.gb, updated_at = now();
  end loop;
  return 'ok';
end $$;

-- Where a player stands on one board, and how many players are on it.
create or replace function public.fd_rank(p_period text, p_key text, p_pid text)
returns table(rank bigint, total bigint) language sql stable security definer set search_path = public as $$
  select (select count(*) from public.fd_scores s
           where s.period = p_period and s.pkey = p_key
             and s.pts > coalesce((select pts from public.fd_scores where pid = p_pid and period = p_period and pkey = p_key), 0)) + 1,
         (select count(*) from public.fd_scores where period = p_period and pkey = p_key);
$$;

-- This week's nations, by the points their players scored.
create or replace function public.fd_nations(p_key text)
returns table(cc text, pts bigint) language sql stable security definer set search_path = public as $$
  select cc, sum(pts)::bigint from public.fd_scores
   where period = 'w' and pkey = p_key and pts > 0
   group by cc order by 2 desc limit 50;
$$;

-- This week's guilds.
create or replace function public.fd_guilds(p_key text)
returns table(gid text, name text, tag text, col text, pts bigint, races bigint, members bigint)
language sql stable security definer set search_path = public as $$
  select gid, max(gn), max(gt), max(gc), sum(pts + gb)::bigint, sum(races)::bigint, count(*)
    from public.fd_scores
   where period = 'w' and pkey = p_key and gid is not null
   group by gid order by 5 desc limit 50;
$$;

grant execute on function public.fd_submit(text, text, jsonb)  to anon, authenticated;
grant execute on function public.fd_rank(text, text, text)     to anon, authenticated;
grant execute on function public.fd_nations(text)               to anon, authenticated;
grant execute on function public.fd_guilds(text)                to anon, authenticated;
