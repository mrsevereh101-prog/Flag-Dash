-- Race Your Flag: uploaded profile pictures.
-- Run this once in Supabase: SQL Editor -> New query -> paste everything -> Run.
-- Safe to run again. Run leaderboard.sql (updated version) too, so the boards can show the pictures.
--
-- Pictures live in a public storage bucket called "avatars", one folder per signed-in player:
--   avatars/<their user id>/<time>.jpg
-- The game shrinks every picture to a small 160 x 160 JPEG before uploading, and the bucket
-- refuses anything else (only JPEG, at most 64 KB). Players can only add, change or remove
-- files in their own folder. Anyone can view them (they show on the leaderboards).

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('avatars', 'avatars', true, 65536, array['image/jpeg'])
on conflict (id) do update set public = true, file_size_limit = 65536, allowed_mime_types = array['image/jpeg'];

drop policy if exists "avatars: add my own"    on storage.objects;
drop policy if exists "avatars: change my own" on storage.objects;
drop policy if exists "avatars: remove my own" on storage.objects;
create policy "avatars: add my own" on storage.objects for insert to authenticated
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "avatars: change my own" on storage.objects for update to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "avatars: remove my own" on storage.objects for delete to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);

-- Reports: when a player reports a picture it is hidden for them at once, and the report is
-- kept here for you to check. To remove a bad picture: Storage -> avatars -> open the folder
-- named in the report -> delete the file.
create table if not exists public.fd_pic_reports (
  id       bigserial primary key,
  pic      text not null check (char_length(pic) <= 80),
  by_id    uuid not null references auth.users(id) on delete cascade,
  created  timestamptz not null default now(),
  unique (pic, by_id)
);
alter table public.fd_pic_reports enable row level security;
revoke all on public.fd_pic_reports from anon, authenticated;
grant insert on public.fd_pic_reports to authenticated;
grant usage on sequence public.fd_pic_reports_id_seq to authenticated;
drop policy if exists "report a picture" on public.fd_pic_reports;
create policy "report a picture" on public.fd_pic_reports for insert to authenticated with check (by_id = auth.uid());

-- Pictures with reports, most reported first (read it in the SQL editor: select * from fd_pic_report_list;)
create or replace view public.fd_pic_report_list as
  select pic, count(*) as reports, max(created) as last_report
    from public.fd_pic_reports group by pic order by 2 desc, 3 desc;
revoke all on public.fd_pic_report_list from anon, authenticated;
