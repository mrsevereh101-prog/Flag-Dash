-- Race Your Flag: player accounts (save progress to an account).
-- Run this once in Supabase: SQL Editor -> New query -> paste everything -> Run.
-- Safe to run again.
--
-- Sign-in itself is handled by Supabase Auth (Google and email links).
-- This table keeps each signed-in player's saved game: coins, purchases, perks, settings, layout.
-- Players can only ever read or change their own row.

create table if not exists public.fd_profiles (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  constraint fd_profiles_size check (pg_column_size(data) < 300000)
);

alter table public.fd_profiles enable row level security;
revoke all on public.fd_profiles from anon;
grant select, insert, update, delete on public.fd_profiles to authenticated;

drop policy if exists "read own save"   on public.fd_profiles;
drop policy if exists "create own save" on public.fd_profiles;
drop policy if exists "update own save" on public.fd_profiles;
drop policy if exists "delete own save" on public.fd_profiles;
create policy "read own save"   on public.fd_profiles for select to authenticated using (auth.uid() = user_id);
create policy "create own save" on public.fd_profiles for insert to authenticated with check (auth.uid() = user_id);
create policy "update own save" on public.fd_profiles for update to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "delete own save" on public.fd_profiles for delete to authenticated using (auth.uid() = user_id);

-- "Delete my account" in the game: removes the player's login and their saved game.
create or replace function public.fd_delete_me()
returns text language plpgsql security definer set search_path = public as $$
begin
  if auth.uid() is null then return 'signed out'; end if;
  delete from auth.users where id = auth.uid();
  return 'deleted';
end $$;
revoke all on function public.fd_delete_me() from public, anon;
grant execute on function public.fd_delete_me() to authenticated;

-- How many players have accounts. Run:  select * from fd_accounts;
create or replace view public.fd_accounts with (security_invoker = true) as
  select count(*) as players_with_accounts,
         count(*) filter (where updated_at > now() - interval '7 days') as active_last_7_days
  from public.fd_profiles;
revoke all on public.fd_accounts from anon, authenticated;
