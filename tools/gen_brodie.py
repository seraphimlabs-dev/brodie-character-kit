#!/usr/bin/env python3
"""Generate a costumed Brodie in the flat sticker style, colour-checked.

Sends both canon references plus the CANON block below to Gemini image, then runs
check_cream on the result. If the body drifted (usually pink), it is snapped back
with fix_cream and re-checked. The raw output is kept beside it as *.raw.png.

Usage: GEMINI_API_KEY=... gen_brodie.py out.png "<costume + pose>" [aspect=1:1]
Example:
  gen_brodie.py chef.png "Brodie as a macros coach: tall white chef's hat, holding a
  wooden spoon up in his right fist, left hand on hip, big grin."
"""
import base64, json, os, sys, time, urllib.request
from pathlib import Path
from check_cream import measure, verdict
from fix_cream import fix

KIT = Path(__file__).resolve().parent.parent
REFS = [KIT / "reference/brodie-flex.png", KIT / "reference/brodie-sit-wave.png"]
MODEL = os.environ.get("BRODIE_IMAGE_MODEL", "gemini-3-pro-image")

SPEC = json.loads((KIT / "brodie.json").read_text())
CANON = " " + SPEC["prompt"]["canon"]


def call(prompt, aspect):
    key = os.environ["GEMINI_API_KEY"]
    parts = [{"text": prompt + CANON}] + [
        {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(r.read_bytes()).decode()}}
        for r in REFS]
    body = json.dumps({"contents": [{"parts": parts}], "generationConfig": {
        "responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                body, {"x-goog-api-key": key, "content-type": "application/json"})
            r = json.load(urllib.request.urlopen(req, timeout=240))
            for p in r["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    return base64.b64decode(p["inlineData"]["data"])
            print("[no image]", json.dumps(r)[:300])
        except urllib.error.HTTPError as e:
            print(f"[http {e.code}]", e.read()[:300]); time.sleep(20 * (attempt + 1))
        except Exception as e:
            print("[err]", e); time.sleep(10)
    raise SystemExit("generation failed")


def main(out, pose, aspect="1:1"):
    out = Path(out)
    raw = out.with_suffix(".raw.png")
    raw.write_bytes(call(pose, aspect))
    fill, _ = measure(raw)
    de, problems = verdict(fill) if fill is not None else (0, ["no cream body found"])
    if not problems:
        out.write_bytes(raw.read_bytes()); print("[pass]", out); return
    print("[drift]", "; ".join(problems), "-> fixing")
    fix(raw, out)
    fill, _ = measure(out)
    print("[after fix]", verdict(fill))


if __name__ == "__main__":
    main(*sys.argv[1:4])
