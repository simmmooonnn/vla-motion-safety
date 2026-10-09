# -*- coding: utf-8 -*-
# Assemble the release upload script (q_rel2.sh): each file written beside the builder via tmp + mv, then build + post in the
# background. Sources: the generator's pool membership, the tools mirror (recompute, scoring, golden test), the builders, and the
# frozen pre-registration (shipped as PREREG.md).
import pathlib
R = pathlib.Path(r"E:\Research\Robotics-Safety")
F = [("release_pool_membership.json", R / "_scratch" / "pool_membership.json"),
     ("release_recompute_table3.py", R / "docs/overleaf_iclr/tools/recompute_table3.py"),
     ("release_SCORING.md", R / "docs/overleaf_iclr/tools/SCORING.md"),
     ("release_PREREG.md", R / "docs/prereg_2026-10-07.md"),
     ("release_PREREG_T2.md", R / "docs/prereg_2026-10-08_t2.md"),
     ("release_PREREG_T2B.md", R / "docs/prereg_2026-10-08_t2b.md"),
     ("release_PREREG_T2C.md", R / "docs/prereg_2026-10-08_t2c.md"),
     ("release_golden_test.py", R / "docs/overleaf_iclr/tools/golden_test.py"),
     ("build_release.sh", R / "_scratch/build_release.sh"),
     ("release_post.sh", R / "_scratch/release_post.sh")]
out = ["cd /home/data/zzhao140/zijian || exit 1"]
for name, src in F:
    body = src.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "__EOF_X__" not in body
    out += [f"cat > {name}.tmp <<'__EOF_X__'", body.rstrip("\n"), "__EOF_X__", f"mv {name}.tmp {name}"]
out.append("(bash build_release.sh > build_release.out 2>&1; bash release_post.sh > release_post.out 2>&1) < /dev/null > /dev/null 2>&1 &")
out.append("echo launched")
(R / "_scratch/q_rel2.sh").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
print("ok", len(out))
