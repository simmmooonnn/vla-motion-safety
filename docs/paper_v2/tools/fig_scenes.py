# Scene strip for Sec. 4.1: the tabletop work surfaces and the humanoid corridor.
#   python _scratch/fig_scenes.py            -> docs/paper_v2/figures/fig_scenes.png
# Panels come from single frames of recorded episodes. Each entry: (label, video, frame index, crop box in source pixels).
# When the as-scored stills (capsule body) exist under demos_2026-10-11/raw/, they are used; otherwise the reel frames.
import os, sys
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont, ImageSequence

ROOT = "E:/Research/Robotics-Safety"
RAW = ROOT + "/demos_2026-10-11/raw"
R02 = ROOT + "/demos_2026-10-02"
OUT = ROOT + "/docs/paper_v2/figures/fig_scenes.png"


def frame(path, idx):
    if path.lower().endswith(".gif"):
        fr = [f.convert("RGB").copy() for f in ImageSequence.Iterator(Image.open(path))]
        return fr[min(idx, len(fr) - 1)]
    r = imageio.get_reader(path)
    n = r.count_frames()
    im = Image.fromarray(r.get_data(min(idx, n - 1)))
    r.close()
    return im


def pick(label_new, fallback):
    p = RAW + "/" + label_new + ".mp4"
    return (p, None) if os.path.exists(p) else fallback


PANELS = [
    ("dining table", pick("r20v4_still_dining_cap", (R02 + "/2_orientation/T4_load_tilt__neutral_instruction__dining.mp4", 40)), 60),
    ("kitchen counter", pick("r20v4_still_kitchen_cap", (R02 + "/5_scene_diversity/scene__kitchen_counter.mp4", 60)), 60),
    ("drawer kitchen", pick("r20v4_still_drawer_cap", (R02 + "/5_scene_diversity/scene__drawer_kitchen.mp4", 60)), 60),
    ("office desk", pick("r20v4_still_office_cap", (R02 + "/2_orientation/T4_load_tilt__keep_hot_coffee_upright__office.mp4", 48)), 60),
    ("packing station", pick("r20v4_still_packing_cap", (R02 + "/5_scene_diversity/scene__industrial_packing_station.mp4", 60)), 60),
    ("humanoid corridor", (R02 + "/4_dynamics/T6_dynamics__G1_person_crossing_corridor__seed42.mp4", 280), 280),
]

if __name__ == "__main__":
    W, H = 640, 400                      # panel size in pixels (16:10 crop of the 16:9 frame)
    pad, lab = 10, 92
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 62)
    sheet = Image.new("RGB", (len(PANELS) * W + (len(PANELS) - 1) * pad, H + lab), "white")
    dr = ImageDraw.Draw(sheet)
    for i, (name, (path, idx), default_idx) in enumerate(PANELS):
        im = frame(path, default_idx if idx is None else idx)
        w, h = im.size
        cw = int(h * W / H)
        im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h)).resize((W, H), Image.LANCZOS)
        x = i * (W + pad)
        sheet.paste(im, (x, 0))
        dr.text((x + W / 2, H + lab / 2), name, font=f, fill=(0, 0, 0), anchor="mm")
    sheet.save(OUT, optimize=True)
    print(OUT, sheet.size, os.path.getsize(OUT) // 1024, "KB")
