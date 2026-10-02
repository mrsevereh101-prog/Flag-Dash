# Flag Dash: where we left off

Game: https://mrsevereh101-prog.github.io/Flag-Dash/
Supabase project: hzzqnwzsasuwjafmsgqh

## Done
- Online play through Supabase Realtime (rooms, lobby, races, Flag Challenge online)
- Worldwide leaderboards (`supabase/leaderboard.sql`, already run)
- Play counts (`supabase/plays.sql`)
- Rivals in the plaza, Flag Challenge mode, hero perks, random Quick Race tracks
- Neon plaza with day/night, weekly top 15 flags
- Race Desk in a locker room, one equipped perk per race, store button on the home screen
- Accounts with a soft gate (code is live; setup below still needed)

## To finish sign-in (accounts)
1. [ ] Run `supabase/accounts.sql` in the Supabase SQL editor (click "Run query" on the warning).
2. [ ] Supabase > Authentication > URL Configuration
   - Site URL: `https://mrsevereh101-prog.github.io/Flag-Dash/`
   - Redirect URLs: add `https://mrsevereh101-prog.github.io/Flag-Dash/**`
3. [ ] Google Cloud (project "Flag Dash") > Google Auth Platform
   - [x] Consent screen (Branding) set up
   - [ ] Audience > Publish app (so anyone can sign in, not just test users)
   - [ ] Clients > Create client > Web application
     - Authorized JavaScript origin: `https://mrsevereh101-prog.github.io`
     - Authorized redirect URI: `https://hzzqnwzsasuwjafmsgqh.supabase.co/auth/v1/callback`
     - Save the Client ID and Client secret (download the JSON)
4. [ ] Supabase > Authentication > Sign In / Providers > Google: turn on, paste Client ID + secret, Save.
   Keep the Client secret private (only in Supabase).
5. [ ] Test: open the game, tap the person button, try "Continue with Google" and the email link.

## Later
- [ ] Privacy policy page + link on the sign-in screen (needed now that emails are collected)
- [ ] Custom email sender (SMTP, e.g. Resend) before a wide launch; Supabase's built-in sender only allows a few emails an hour
- [ ] Decide on screen-layout editing: keep for everyone (option 1), owner-only, or a built-in default layout
