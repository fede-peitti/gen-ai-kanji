import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image
import io


def collect_paths(elem):
    """Recursively collect all <path> elements, stripping namespaces."""
    paths = []
    for child in elem:
        tag = child.tag.split("}")[-1]  # remove namespace
        if tag == "path":
            paths.append(child)
        elif tag == "g":
            paths.extend(collect_paths(child))
    return paths


def render_kanji_svg_to_png(kanji_element, size=128):
    """
    Convert a KanjiVG <kanji> element to a high-quality grayscale PNG.
    - White background
    - Smooth strokes
    - Antialiased when resizing
    """
    kanji_copy = ET.fromstring(ET.tostring(kanji_element))

    # Strip namespaces
    def strip_ns(elem):
        elem.tag = elem.tag.split("}")[-1]
        for c in elem:
            strip_ns(c)

    strip_ns(kanji_copy)

    # Collect all <path> elements
    paths = collect_paths(kanji_copy)
    if not paths:
        raise ValueError("No paths found in kanji element!")

    # Build SVG content
    svg_paths = ""
    for p in paths:
        d = p.attrib.get("d")
        if d:
            svg_paths += (
                f'<path d="{d}" stroke="#000000" fill="none" stroke-width="2"/>'
            )

    # Full SVG
    svg_data = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="109" height="109" viewBox="0 0 109 109">
        <rect width="109" height="109" fill="white"/>
        {svg_paths}
    </svg>
    """

    # Render at higher resolution for smoothness
    high_res = 1080
    png_bytes = cairosvg.svg2png(
        bytestring=svg_data.encode("utf-8"),
        output_width=high_res,
        output_height=high_res,
    )

    # Open with PIL, convert to grayscale, downscale with antialiasing
    img = Image.open(io.BytesIO(png_bytes)).convert("L")
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    return img
