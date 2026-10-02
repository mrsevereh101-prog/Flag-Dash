-- Flag Dash: count who plays (anonymous).
-- Run this once in Supabase: SQL Editor -> New query -> paste everything -> Run.
-- Safe to run again.
--
-- Each row is one event from one device: the game being opened, or a race being finished.
-- pid is the random device ID the game already uses for the leaderboard. No names, no emails, no IP addresses.

create table if not exists public.fd_plays (
  id      bigint generated always as identity primary key,
  pid     text not null check (pid ~ '^p[a-z0-9]{8,16}$'),
  event   text not null check (event in ('open','race')),
  mode    text check (mode is null or mode ~ '^[a-z0-9-]{1,16}$'),
  track   text check (track is null or track ~ '^[a-z0-9-]{1,16}$'),
  device  text check (device is null or device in ('phone','tablet','computer')),
  at      timestamptz not null default now()
);
create index if not exists fd_plays_at on public.fd_plays (at desc);
create index if not exists fd_plays_pid on public.fd_plays (pid, at desc);

-- Players can't read or change this table. Only you can see it, in the Supabase dashboard.
alter table public.fd_plays enable row level security;
revoke all on public.fd_plays from anon, authenticated;

-- The game logs through this function. A device can log at most 30 events an hour.
create or replace function public.fd_log_play(p_pid text, p_event text, p_mode text, p_track text, p_device text)
returns text language plpgsql security definer set search_path = public as $$
begin
  if p_pid !~ '^p[a-z0-9]{8,16}$' or p_event not in ('open','race') then return 'bad'; end if;
  if (select count(*) from public.fd_plays where pid = p_pid and at > now() - interval '1 hour') >= 30 then return 'slow'; end if;
  insert into public.fd_plays(pid, event, mode, track, device)
  values (p_pid, p_event,
          case when p_mode  ~ '^[a-z0-9-]{1,16}$' then p_mode  end,
          case when p_track ~ '^[a-z0-9-]{1,16}$' then p_track end,
          case when p_device in ('phone','tablet','computer') then p_device end);
  return 'ok';
end $$;
revoke all on function public.fd_log_play(text,text,text,text,text) from public;
grant execute on function public.fd_log_play(text,text,text,text,text) to anon, authenticated;

-- Ready-made summaries. Open them in Table Editor (they're under "Views"), or run:  select * from fd_daily;
create or replace view public.fd_daily with (security_invoker = true) as
  select (at at time zone 'America/New_York')::date as day,
         count(distinct pid)                         as players,
         count(*) filter (where event = 'open')      as opens,
         count(*) filter (where event = 'race')      as races,
         count(distinct pid) filter (where device = 'phone') as on_phones
  from public.fd_plays group by 1 order by 1 desc;

create or replace view public.fd_totals with (security_invoker = true) as
  select count(distinct pid)                         as all_time_players,
         count(*) filter (where event = 'race')      as all_time_races,
         count(distinct pid) filter (where at > now() - interval '7 days') as players_last_7_days,
         count(distinct pid) filter (where at > now() - interval '1 day')  as players_last_24_hours
  from public.fd_plays;

create or replace view public.fd_modes with (security_invoker = true) as
  select coalesce(mode,'?') as mode, count(*) as races, count(distinct pid) as players
  from public.fd_plays where event = 'race' group by 1 order by 2 desc;

revoke all on public.fd_daily, public.fd_totals, public.fd_modes from anon, authenticated;
