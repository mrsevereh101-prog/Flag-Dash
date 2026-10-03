# Flag Dash heroes: cartoon 3D prompts

Prompts to recreate the 5 heroes in the cartoon 3D look. Each hero has two prompts:

- **Concept sheet**: for an image tool (ChatGPT image, Midjourney, Leonardo). Make this first, so you can see and approve the look.
- **3D model**: for a text-to-3D tool (Meshy, Tripo, Rodin). You can also upload the approved concept sheet as an image and use this text with it.

Always paste the **shared style** block first, then the hero's prompt. That keeps all five heroes looking like one set.

---

## Shared style (paste before every hero)

> Stylized cartoon 3D game character for a family-friendly mobile running game called Flag Dash. Chibi-leaning proportions: head about 1/4 of body height, big expressive eyes, friendly determined face, chunky hands and feet. Clean toon shading with 2–3 flat tones per color, crisp dark brown outline, bright saturated colors, simple readable shapes, no tiny details. Athletic running build. Each hero carries a small rectangular flag on a thin silver pole strapped to their back, rising above the head; the flag is plain white (the game puts the player's country on it). Neutral light grey background, soft even lighting, no text, no logo.

**Concept sheet ending** (add after the hero prompt):

> Character turnaround sheet: front, side, back and 3/4 view, full body, standing A-pose, same scale in every view.

**3D model ending** (add after the hero prompt):

> Game-ready low-poly 3D model, A-pose, about 8,000–12,000 triangles, clean quad-friendly topology, hand-painted flat color texture (no realistic materials, no metal reflections), weapon as a separate object, ready for auto-rigging, export as GLB.

**Avoid** (use as the negative prompt where the tool has one):

> realistic, photoreal, gritty, gore, blood, scary, horror, sexualized, overly detailed armor, noisy textures, glossy metal, text, watermark, extra limbs, cropped feet

---

## 1. Samurai: power Slash, perk Bushido (gets up faster)

> A samurai runner with warm tan skin and short black hair. Wears black and deep-red lacquered lamellar armor: a segmented chest plate, layered shoulder plates and a short layered skirt, with red cords tied at the knees. Dark helmet (kabuto) with a gold rim, a gold crescent crest on the front and red side flaps. Small black mustache, strong angled eyebrows, focused confident grin. Holds a gleaming katana in the right hand; a second sheathed sword at the left hip. Black fitted trousers and black sandals with socks. Colors: black, deep red, gold accents.

## 2. Warrior: power Lightning, perk Unstoppable (smashes through walls)

> A big, broad-shouldered warrior runner with deep brown skin and black cornrow braids. Bare muscular arms and legs. Brown leather chest armor with a wide dark leather belt, and a navy-blue patterned kilt. Necklace of white and red bone beads. Brass armbands on the upper arms and forearms, with turquoise rings. Round brown hide shield on the left forearm and a long wooden spear with a steel tip in the right hand. Brown leather shin wraps and boots. Proud, fearless smile. Small blue-white lightning sparks around the spear tip. Colors: warm brown, navy, brass, turquoise.

## 3. Archer: power Wind, perk Full Quiver (starts with an item)

> A slim, quick archer runner, a young woman with light skin and long brown hair worn in one braid over the shoulder. Dark green hood pushed back onto her shoulders. Quilted green-and-brown padded tunic, brown leather shoulder guards and leather knee guards, a dark green cape. Wooden bow in the left hand and a leather quiver of arrows on her back, beside the flag pole. Brown fitted trousers and soft leather boots. Bright, playful look, light freckles. A few pale-green wind swirls around her feet. Colors: forest green, leather brown, cream.

## 4. Elf: power Trees, perk Light Feet (never slips)

> A graceful elf runner, a young woman with fair skin, green eyes and long silver-white hair with two braids bound by gold rings. Pointed ears. Thin gold circlet across the forehead with a small pointed gem. Moss-green, leaf-shaped shoulder pieces with gold trim, a green tunic with long front and back cloth panels, olive knee guards and a dark green cape. Elegant wooden bow with gold tips in the left hand, a slim silver sword in the right, quiver on the back. Calm, kind smile. Tiny leaves floating around her. Colors: leaf green, silver-white, gold.

## 5. Dwarf: power Earthquake, perk Low Rider (runs under barricades)

> A short, very wide dwarf runner, about two-thirds the height of the others, with short sturdy legs and big boots. Ruddy skin, rosy cheeks, bushy eyebrows and a huge bushy orange beard with two braids ending in silver rings. Rounded steel helmet with a gold rim, a nose guard and two curved ivory horns. Steel shoulder plates with gold trim, a thick grey fur collar and fur belt with a gold buckle, and a chainmail skirt. Round steel shield with a ram's-head emblem on the left arm, and a wooden axe with a rune-carved head in the right hand. Jolly, stubborn grin. Colors: steel grey, orange, brown, gold.

---

## Tips

- **Same look across the set:** generate the Samurai first. Once you like it, add "in exactly the same art style as the attached image" and attach it when you make the other four.
- **Keep the flag plain white:** the game paints each player's country flag onto it.
- **Size:** the dwarf is shorter and wider on purpose (his perk lets him run under barricades). The warrior is the broadest of the tall heroes, and the archer and elf are the slimmest.
- **What I need from you:** the GLB file for each hero. Rigged and animated is best (run, jump, slide, fall, cheer), but rigged-only also works: I can drive the running motion in the game. Bringing them in is a code change I'd do later, after you approve the look.
