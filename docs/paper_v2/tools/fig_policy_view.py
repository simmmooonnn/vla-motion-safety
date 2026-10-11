# What the policies' cameras show (App. B): frames of the DROID embodiment's external and wrist cameras, written by the
# camera probe (a scripted carry whose only addition is saving the two images every policy receives).
#   python _scratch/fig_policy_view.py           -> docs/paper_v2/figures/fig_policy_view.jpg
#   python _scratch/fig_policy_view.py sheets    -> contact sheets of every probe label under _scratch/tmp/rev3/camprobe_sheets/
# Each panel: (caption, probe label, camera tag, step). Frames are 1280 x 720; the policy adapters letterbox them to 224 x 224.
import os, sys, glob, re
from PIL import Image, ImageDraw, ImageFont

ROOT = "E:/Research/Robotics-Safety"
SRC = ROOT + "/_scratch/tmp/rev3/camprobe"
OUT = ROOT + "/docs/paper_v2/figures/fig_policy_view.jpg"

# row 1: the still bystander at each work surface (external camera, first frame of the episode)
# row 2: the moving bodies, the keep-out marker and the wrist camera
PANELS = [
    ("(a) dining, right", "camv_din_serving_R", "ext", None),
    ("(b) dining, left", "camv_din_L", "ext", None),
    ("(c) office desk", "camv_office", "ext", None),
    ("(d) packing station", "camv_packing", "ext", None),
    ("(e) kitchen counter", "camv_kitchen", "ext", None),
    ("(f) drawer kitchen", "camv_drawer", "ext", None),
    ("(g) crossing forearm", "camv_din_hand", "ext", "mid"),
    ("(h) passer-by", "camv_din_walker", "ext", "mid"),
    ("(i) hot-plate marker", "camv_kitchen_marker", "ext", None),
    ("(j) wrist view of (a)", "camv_din_serving_R", "wrist", "late"),
    ("(k) wrist view of (e)", "camv_kitchen", "wrist", "late"),
    ("(l) (a), human mesh", "camv_din_serving_R_mesh", "ext", None),
]
STEP = {("camv_din_hand", "ext"): 32, ("camv_din_walker", "ext"): 47, ("camv_din_serving_R", "wrist"): 137,
        ("camv_kitchen", "wrist"): 107}   # (label, tag) -> step, chosen from the contact sheets


def frames(label, tag):
    fs = sorted(glob.glob("%s/%s__%s__t*.jpg" % (SRC, label, tag)))
    return [(int(re.search(r"__t(\d+)\.jpg$", f).group(1)), f) for f in fs]


def pick(label, tag, when):
    fr = frames(label, tag)
    if not fr:
        return None
    if (label, tag) in STEP:
        want = STEP[(label, tag)]
        return min(fr, key=lambda tf: abs(tf[0] - want))[1]
    if when is None:
        return fr[0][1]
    if when == "mid":
        return fr[len(fr) // 2][1]
    return fr[min(len(fr) - 1, (2 * len(fr)) // 3)][1]


def sheets():
    od = ROOT + "/_scratch/tmp/rev3/camprobe_sheets"
    os.makedirs(od, exist_ok=True)
    labels = sorted(set(os.path.basename(f).split("__")[0] for f in glob.glob(SRC + "/*.jpg")))
    for lb in labels:
        fe, fw = frames(lb, "ext"), frames(lb, "wrist")
        n = max(len(fe), len(fw))
        w, h = 320, 180
        sh = Image.new("RGB", (n * w, 2 * h), "white")
        dr = ImageDraw.Draw(sh)
        for j, fr in enumerate([fe, fw]):
            for i, (t, f) in enumerate(fr):
                sh.paste(Image.open(f).resize((w, h), Image.LANCZOS), (i * w, j * h))
                dr.text((i * w + 4, j * h + 3), "%s t=%d" % ("ext" if j == 0 else "wrist", t), fill=(255, 255, 0))
        sh.save("%s/%s.jpg" % (od, lb), quality=85)
        print(lb, len(fe), len(fw))


def main():
    cols = 6
    w, h = 640, 360
    pad, lab = 10, 92
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
    rows = (len(PANELS) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * pad, rows * (h + lab) + (rows - 1) * 6), "white")
    dr = ImageDraw.Draw(sheet)
    miss = []
    for i, (cap, lb, tag, when) in enumerate(PANELS):
        p = pick(lb, tag, when)
        x, y = (i % cols) * (w + pad), (i // cols) * (h + lab + 6)
        if p is None:
            miss.append(lb)
            dr.rectangle([x, y, x + w, y + h], outline=(160, 160, 160))
        else:
            sheet.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, y))
        dr.text((x + w / 2, y + h + lab / 2), cap, font=f, fill=(0, 0, 0), anchor="mm")
    sheet.save(OUT, quality=90, optimize=True)
    print(OUT, sheet.size, os.path.getsize(OUT) // 1024, "KB", "missing:", miss)


if __name__ == "__main__":
    if sys.argv[1:] == ["sheets"]:
        sheets()
    else:
        main()
