# Flag Dash: where we left off

Game: https://mrsevereh101-prog.github.io/Flag-Dash/
Supabase project: hzzqnwzsasuwjafmsgqh

## Done
- Online play through Supabase Realtime (rooms, lobby, races, Flag Challenge online)
- Worldwide leaderboards (`supabase/leaderboard.sql`, already run)
- Play counts (`supabase/plays.sql`, run Oct 2)
- Rivals in the plaza, Flag Challenge mode, hero perks, random Quick Race tracks
- Neon plaza with day/night, weekly top 15 flags
- Race Desk in a locker room, one equipped perk per race, store button on the home screen
- Accounts with a soft gate: Google sign-in tested and working (Oct 2)

## To finish sign-in (accounts)
1. [x] Run `supabase/accounts.sql` in the Supabase SQL editor (click "Run query" on the warning).
2. [x] Supabase > Authentication > URL Configuration
   - Site URL: `https://mrsevereh101-prog.github.io/Flag-Dash/`
   - Redirect URLs: add `https://mrsevereh101-prog.github.io/Flag-Dash/**`
3. [ ] Google Cloud (project "Flag Dash") > Google Auth Platform
   - [x] Consent screen (Branding) set up
   - [x] Branding: home page, privacy policy link, authorized domains (mrsevereh101-prog.github.io, hzzqnwzsasuwjafmsgqh.supabase.co), developer email, Save
   - [x] Audience > Publish app (so anyone can sign in, not just test users)
   - [x] Clients > Create client > Web application (replace the secret shown in chat with a new one)
     - Authorized JavaScript origin: `https://mrsevereh101-prog.github.io`
     - Authorized redirect URI: `https://hzzqnwzsasuwjafmsgqh.supabase.co/auth/v1/callback`
     - Save the Client ID and Client secret (download the JSON)
4. [x] Supabase > Authentication > Sign In / Providers > Google: turn on, paste Client ID + secret, Save.
   Keep the Client secret private (only in Supabase).
5. [x] Test: open the game, tap the person button, try "Continue with Google" and the email link.

## Later
- [ ] Rewrite hero speech lines: edit `HERO-SPEECH.md` and send it back
- [ ] Better hero graphics (more detailed models), when there's time
- [x] Privacy policy: https://mrsevereh101-prog.github.io/Flag-Dash/privacy.html (contact mr.severeh65@gmail.com)
- [ ] Custom email sender (SMTP, e.g. Resend) before a wide launch; Supabase's built-in sender only allows a few emails an hour
- [ ] Decide on screen-layout editing: keep for everyone (option 1), owner-only, or a built-in default layout
