# Race Your Flag (formerly Flag Dash): where we left off

Game: https://mrsevereh101-prog.github.io/race-your-flag/
Supabase project: hzzqnwzsasuwjafmsgqh

## Done
- Online play through Supabase Realtime (rooms, lobby, races, Flag Challenge online)
- Worldwide leaderboards (`supabase/leaderboard.sql`, already run)
- Play counts (`supabase/plays.sql`, run Oct 2)
- Rivals in the plaza, Flag Challenge mode, hero perks, random Quick Race tracks
- Neon plaza with day/night, weekly top 15 flags
- Race Desk in a locker room, one equipped perk per race, store button on the home screen
- Accounts with a soft gate: Google sign-in tested and working (Oct 2)
- 3D icons live (Oct 8): 168 pictures in `img/icons/` replace the emoji across the game.
  To redo one: make a picture with its prompt in `3D-ITEMS.md`, cut it out with `art/cut.py`
  (green or magenta screen), and save it over `img/icons/<file>.webp`. Original pictures are in `art/sheets/`.

## To finish sign-in (accounts)
1. [x] Run `supabase/accounts.sql` in the Supabase SQL editor (click "Run query" on the warning).
2. [x] Supabase > Authentication > URL Configuration
   - Site URL: `https://mrsevereh101-prog.github.io/race-your-flag/`
   - Redirect URLs: add `https://mrsevereh101-prog.github.io/race-your-flag/**`
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

## To finish the rename (Flag Dash -> Race Your Flag)
- [x] GitHub repo renamed to `race-your-flag`; game links updated
- [x] Supabase > Authentication > URL Configuration: new Site URL and Redirect URL
- [ ] Test "Continue with Google" at https://mrsevereh101-prog.github.io/race-your-flag/
- [ ] Google Cloud > Google Auth Platform > Branding (https://console.cloud.google.com/auth/branding): app name `Race Your Flag`, home page `https://mrsevereh101-prog.github.io/race-your-flag/`, privacy link `https://mrsevereh101-prog.github.io/race-your-flag/privacy.html`, Save
- [ ] Optional: new public repo `Flag-Dash` so the old link forwards to the new one (ask Claude to add the redirect page)
- [ ] Record in ElevenLabs: "Welcome to Race Your Flag!", "Choose your flag.", "Pick your runner.", "Choose your perk."

## To turn on uploaded profile pictures
1. [x] Run `supabase/avatars.sql` in the Supabase SQL editor (creates the "avatars" storage bucket, upload rules and the report list).
2. [x] Run the updated `supabase/leaderboard.sql` (adds the picture columns).
3. Checking reports: SQL editor -> `select * from fd_pic_report_list;` To remove a picture: Storage -> avatars -> the folder in the report -> delete the file.

## To turn on Friends & Inbox
1. [ ] Run `supabase/social.sql` in the Supabase SQL editor (New query, paste everything, Run; click "Run query" if a warning shows).
2. [ ] Test with a friend: both tap **Online > Find a Race**, then use the 👥 button during the race to add each other and send a message.

## Private for now (Oct 8)
- The game shows a "Coming soon" screen to everyone except accounts on the developer list (`supabase/devs.sql`).
  It also asks search engines not to list the site. To open the game to everyone again, remove the gate
  (the `#gate` screen and `renderGate()` in index.html) and the robots meta tag.

## Developer accounts
- Run `supabase/devs.sql` once in the Supabase SQL editor, then the `insert` line in it with the email you sign in with.
- In the game: sign in, Settings, Developer mode. Everything unlocks in a sandbox that never syncs or posts scores;
  switching it off brings back your real save.

## To do (added Oct 10)
- [ ] **Guild wars**: guilds race against each other for a season, with a guild leaderboard and rewards for the winning guild.
- [ ] **Guild perks**: bonuses a guild unlocks together (for example more coins or faster power recharge for every member), bought with guild points.
- [ ] **Gifts to each other**: players can already send room items to friends (they arrive in the inbox). Next: send other things too, like perks, coins or skins.
- [ ] **Guild custom flags**: each guild designs its own flag (colors, emblem), shown in guild races and on members.
- [ ] **Flag capes**: a cape in your country's flag (or your guild's flag) worn on the back, as attire.
- [ ] **New heroes** (each needs a look, a power, a perk, speech lines and a voice):
  - [ ] Knight
  - [ ] Viking
  - [ ] Shaolin monk
  - [ ] Indian warrior
  - [ ] Queen of All Beasts: a Black woman hero who commands animals

## Flag capes (on hold, added Oct 10)
- Heroes wear their flag as a cape instead of the flag on their shoulder. Build as a preview first.
- Home screen: turn the runner slightly so the cape shows.
- Wings and jetpack: remove them or replace them with something else (undecided).
- The bought Hero Cape could become a gold trim on the flag cape.

## Flags (added Oct 10)
- [ ] **3D flag icons**: test batch of 6 sent (straight flags on a shiny platter). After the style is chosen, 25 batches of 6 for all 147 flags. The game keeps its current flags until a player earns the 3D one.
- [ ] **Flag perks**: earn a country's 3D flag as a reward, then buy its perks. 3 perks per flag, each unlocked by an achievement with that flag, permanent once bought. Shown with star, gold, diamond and platinum symbols by value. Open questions: how a flag is won, what the perks do, prices, and how the 4 symbols map to 3 perks.
- [ ] **National symbols**: a list of each country's symbols (coat of arms, national animal or bird, national plant) for all 147 countries, checked before use. Ideas: a symbol badge on the 3D flag, the animal as a companion or power effect at platinum, and the symbol as that flag's perk icon.

## Later
- [ ] Rewrite hero speech lines: edit `HERO-SPEECH.md` and send it back
- [ ] Better hero graphics (more detailed models), when there's time
- [x] Privacy policy: https://mrsevereh101-prog.github.io/race-your-flag/privacy.html (contact mr.severeh65@gmail.com)
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
