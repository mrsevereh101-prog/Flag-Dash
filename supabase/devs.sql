-- Race Your Flag: developer accounts.
-- Run once in Supabase: SQL Editor -> New query -> paste everything -> Run. Safe to run again.
--
-- A developer sees a "Developer mode" switch in Settings. It turns the game into a sandbox with every
-- skin, perk, item, attire piece and room item unlocked. The sandbox never syncs to the account and
-- never posts leaderboard scores, and switching it off brings back the real save.
--
-- The list lives only here in the database, so nobody can find it in the game's code.

create table if not exists public.fd_devs (
  uid    uuid primary key references auth.users(id) on delete cascade,
  added  timestamptz not null default now()
);
alter table public.fd_devs enable row level security;
revoke all on public.fd_devs from anon, authenticated;

-- true when the signed-in player is on the list
create or replace function public.fd_is_dev() returns boolean
  language sql stable security definer set search_path = public
  as $$ select exists (select 1 from public.fd_devs where uid = auth.uid()) $$;
revoke all on function public.fd_is_dev() from public;
grant execute on function public.fd_is_dev() to authenticated;

-- To add yourself: take away the two dashes at the start of the next line, put the email you sign in
-- to the game with between the quotes, and run it. (Sign in to the game once first.)
-- insert into public.fd_devs (uid) select id from auth.users where email = 'you@example.com' on conflict do nothing;

-- To see who is on the list:  select d.uid, u.email from public.fd_devs d join auth.users u on u.id = d.uid;
-- To remove someone:          delete from public.fd_devs where uid = (select id from auth.users where email = 'them@example.com');
