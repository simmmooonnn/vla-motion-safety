"""Extract a handful of frames from each still_* viewport video (on chaowei) as downscaled PNGs; videos stay where they are."""
import glob, os, sys
import imageio.v2 as iio
F = "/home/data/zzhao140/zijian/isaac/logs/fr"
OUT = os.path.join(F, "stills_png"); os.makedirs(OUT, exist_ok=True)
for d in sorted(glob.glob(os.path.join(F, "video_still_*"))):
    lb = os.path.basename(d)[len("video_"):]
    vids = sorted(glob.glob(os.path.join(d, "**", "*.mp4"), recursive=True))
    if not vids:
        print(lb, "no video"); continue
    r = iio.get_reader(vids[0]); n = r.count_frames()
    for t in (0.10, 0.30, 0.45, 0.60, 0.75, 0.90):
        k = min(n - 1, int(t * n)); im = r.get_data(k)[::2, ::2]
        iio.imwrite(os.path.join(OUT, f"{lb}_{int(t*100):02d}.png"), im)
    print(lb, "frames", n, "->", OUT)
