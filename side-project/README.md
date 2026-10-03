# Flag Dash style test (side project)

This branch (`style-test`) holds the graphics experiments. It is separate from `main`, so the live game is not affected.

## Test pages (private links, open on claude.ai)
- Cartoon 3D (the real game with a cartoon finish, Sahara Dunes only, new Samurai): https://claude.ai/artifact/V47Kwzpv2hJSutyZZVg4nq
- 2.5D (flat cartoon art, one race on Sahara Dunes): https://claude.ai/artifact/LYNsjLHiHWHuQXcNW5poDx

## Files
- `cartoon-3d.html`: source of the cartoon 3D test (copy of the game + cartoon shading/outlines + the new Samurai with a skeleton built in code)
- `2.5d.html`: source of the 2.5D test
- `HERO-PROMPTS.md`: prompts for all 5 heroes (concept sheet + 3D model)
- `assets/samurai-sheet.webp`: approved Samurai turnaround (with the smile)
- `assets/samurai-front.png`, `-side.png`, `-back.png`: crops to upload to image-to-3D tools
- `assets/samurai-miora.glb`: Samurai made with Miora AI (good model, no skeleton), used in the test
- `assets/samurai-first-try.glb`: first attempt, cut out of a 4-figure file (not used now)

## Where we stopped (Oct 3)
- The Samurai works in the cartoon 3D test: a skeleton is built in code, so he runs, jumps, slides and does the 4 emotes with the game's animations.
- Still rough: a small dark wedge between his legs when he runs; his armor gets no cartoon outline.

## Next time
1. Make the other heroes the same way: one front image in A-pose (attach the Samurai sheet as the style reference), then Miora AI, then send the GLB.
2. Decide: cartoon 3D vs 2.5D.
3. Later: a victory dance per hero, from a short phone video of a person (video-to-motion tools: DeepMotion, Rokoko Vision, Move.ai).
4. Only then bring the new heroes into the real game on `main`.
