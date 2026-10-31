"""Reuse existing barrel/column art with ground-contact origins for scene props.

No pixels are changed. The template assets retain their original origins.
"""
from pathlib import Path
from PIL import Image
import gmyy

ALIASES = {
    "supply_barrel": "spr_barrel_small",
    "water_barrel": "spr_barrel_big",
    "column_fallen": "spr_pillar_fallen",
    "column_broken": "spr_pillar_half",
    "column_whole": "spr_pillar_whole",
}


def main():
    root = Path(gmyy.PROJ).resolve()
    project = gmyy.Project()
    for name, source in ALIASES.items():
        directory = root / "sprites" / source
        meta = gmyy.gm_loads((directory / (source+".yy")).read_text(encoding="utf-8"))
        frames = [Image.open(directory / (frame["name"]+".png")).convert("RGBA") for frame in meta["frames"]]
        # Template collision boxes only cover their bases. Visibility checks
        # need the whole opaque silhouette, excluding the soft baked shadow.
        boxes = [frame.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox() for frame in frames]
        boxes = [box for box in boxes if box]
        visual_bounds = (min(b[0] for b in boxes),min(b[1] for b in boxes),
                         max(b[2] for b in boxes)-1,max(b[3] for b in boxes)-1)
        target = (root / "sprites" / ("spr_"+name)).resolve()
        assert target.is_relative_to(root / "sprites"), target
        gmyy.write_sprite(project, "spr_"+name, frames,
            (meta["sequence"]["xorigin"], meta["bbox_bottom"]),
            "Sprites/Environment", fps=meta["sequence"]["playbackSpeed"], bbox=visual_bounds)
    project.save()
    print("Prepared five existing-art scenery variants with ground origins.")


if __name__ == "__main__":
    main()
