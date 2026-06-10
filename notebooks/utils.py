"""Helpers shared by the tutorial notebooks."""
from __future__ import annotations

import re
import subprocess


def scene_bbox(*image_camera_pairs, session=None, pad=0.05):
    """Lon/lat bounding box covering one or more scenes, as "minlon minlat maxlon maxlat".

    Runs ASP's `camera_footprint` on each (image, camera) pair and unions the
    results. `pad` (degrees) absorbs terrain-induced footprint shift, since the
    footprint is computed on the datum ellipsoid.
    """
    boxes = []
    for image, camera in image_camera_pairs:
        cmd = ["camera_footprint", "--quick", "--datum", "WGS84"]
        if session:
            cmd += ["-t", session]
        cmd += [str(image), str(camera)]
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        m = re.search(
            r"Min: \(([-\d.eE+]+), ([-\d.eE+]+)\) width: ([-\d.eE+]+) height: ([-\d.eE+]+)",
            out,
        )
        if not m:
            raise RuntimeError(f"Could not parse camera_footprint output:\n{out}")
        minlon, minlat, w, h = map(float, m.groups())
        boxes.append((minlon, minlat, minlon + w, minlat + h))
    minlon = min(b[0] for b in boxes) - pad
    minlat = min(b[1] for b in boxes) - pad
    maxlon = max(b[2] for b in boxes) + pad
    maxlat = max(b[3] for b in boxes) + pad
    return f"{minlon:.4f} {minlat:.4f} {maxlon:.4f} {maxlat:.4f}"


def utm_epsg(bbox):
    """EPSG code ("EPSG:326xx" north / "EPSG:327xx" south) of the UTM zone at a bbox center."""
    minlon, minlat, maxlon, maxlat = map(float, bbox.split())
    lon = (minlon + maxlon) / 2
    lat = (minlat + maxlat) / 2
    zone = int((lon + 180) // 6) + 1
    return f"EPSG:{(32600 if lat >= 0 else 32700) + zone}"
