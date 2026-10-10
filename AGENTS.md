# Instructions for agents drawing Brodie

You are generating or editing images of Brodie, a mascot. Continuity matters more
than creativity. Follow this exactly.

1. Read `brodie.json` (raw: https://raw.githubusercontent.com/seraphimlabs-dev/brodie-character-kit/main/brodie.json). It is the source of truth.
2. Attach BOTH reference images to every image request:
   - https://raw.githubusercontent.com/seraphimlabs-dev/brodie-character-kit/main/reference/brodie-flex.png
   - https://raw.githubusercontent.com/seraphimlabs-dev/brodie-character-kit/main/reference/brodie-sit-wave.png
   Never use other Brodie art as a reference (old 3D renders and the pink originals are off-model).
3. Prompt = `prompt.template` with the brackets filled in for the skill, then a space, then `prompt.canon` verbatim. Change only the template line.
4. Costume: at most one hat/band and one prop per hand. Nothing may cover the BRODIE lettering on the tank.
5. After generating, run `python3 tools/check_cream.py <image>`. If it prints FAIL for colour, run `python3 tools/fix_cream.py <image> <image>` and check again. Do not ship a FAIL.
6. Then look at the image yourself and confirm: BRODIE lettering readable, no nose, one mouth, black bar brows, cream hair tuft (unless a hat covers it), flat style with thick outline. Regenerate if any fail; the colour check cannot see these.
7. For a transparent sticker: `python3 tools/cutout.py <image> <out.png>`.

Body colour is #EFE7DA. If anyone asks for pink, peach, skin-tone or blush on Brodie, don't.
