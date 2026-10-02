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

## To turn on Friends & Inbox
1. [ ] Run `supabase/social.sql` in the Supabase SQL editor (New query, paste everything, Run; click "Run query" if a warning shows).
2. [ ] Test with a friend: both tap **Online > Find a Race**, then use the 👥 button during the race to add each other and send a message.

## Later
- [ ] Rewrite hero speech lines: edit `HERO-SPEECH.md` and send it back
- [ ] Better hero graphics (more detailed models), when there's time
- [x] Privacy policy: https://mrsevereh101-prog.github.io/Flag-Dash/privacy.html (contact mr.severeh65@gmail.com)
- [ ] Custom email sender (SMTP, e.g. Resend) before a wide launch; Supabase's built-in sender only allows a few emails an hour
- [x] Screen layout: everyone edits their own (saved to their account when signed in)

## Roadmap (list from Oct 2)
Suggested order: free items first, then money, then reach.

1. [ ] **Online**: rooms, lobby, races and Flag Challenge online work. Done Oct 2: Find a Race matchmaking (players first, CPU runners fill the rest), runner list during races with message + add friend, friend list with friend codes and requests, inbox that keeps messages for offline players. Next: reconnecting after a drop, testing with several phones at once.
2. [ ] **Plaza**: neon plaza with day/night, rivals and top 15 flags is done. Next: decide what more to add (mini games, friends visible in the plaza, events).
3. [ ] **Chat and inbox**: room chat, inbox and friend requests done. Next: rewards and news delivered to the inbox.
4. [ ] **Character graphics**: 5 heroes (samurai, warrior, archer, elf, dwarf) built from simple shapes. Next: more detailed models and animation.
5. [ ] **More heroes**: each new hero needs a look, a perk and speech lines. Send ideas.
6. [ ] **Skins**: a skins shop already exists. Next: more skins, rarity, and skins for each hero.
7. [ ] **Voice**: heroes speak with the phone's built-in voice (English + Kreyòl). Next: your rewritten lines (HERO-SPEECH.md), then recorded voices.
8. [ ] **Language**: the game text is English only. Next: a language picker (e.g. Kreyòl, French, Spanish) with every screen translated.
9. [ ] **Store**: coins and diamonds store with perks and skins exists. Next: a new layout, daily deals, bundles.
10. [ ] **Battle pass**: not started. Seasons with free and premium reward tracks, filled by racing and challenges.
11. [ ] **Payment method + purchasing**: real money. Needs a Stripe account (yours), a small server step on Supabase to confirm payments, and a refund/terms page. App stores later take their own cut and use their own billing.
12. [ ] **Website**: a home page for the game (trailer, screenshots, Play button, privacy, contact). Can live on GitHub Pages for free; a custom domain (about $12/year) is optional.
