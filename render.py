import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image
import io


def collect_paths(elem):
    paths = []
    for child in elem:
        tag = child.tag.split("}")[-1]
        if tag == "path":
            paths.append(child)
        elif tag == "g":
            paths.extend(collect_paths(child))
    return paths


def render_kanji_svg_to_png(kanji_element, size=128):
    """Render KanjiVG element to PNG with smooth strokes at higher resolution."""

    def strip_ns(elem):
        elem.tag = elem.tag.split("}")[-1]
        for c in elem:
            strip_ns(c)

    kanji_copy = ET.fromstring(ET.tostring(kanji_element))
    strip_ns(kanji_copy)

    paths = collect_paths(kanji_copy)
    if not paths:
        raise ValueError("No paths found!")

    svg_content = "".join(
        f'<path d="{p.attrib["d"]}" stroke="#000" fill="none" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        for p in paths
    )

    # Render large internal canvas
    internal_size = 512
    svg_data = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{internal_size}" height="{internal_size}" viewBox="0 0 109 109">
        <rect width="100%" height="100%" fill="white"/>
        {svg_content}
    </svg>
    """

    png_bytes = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    img = Image.open(io.BytesIO(png_bytes)).convert("L")

    # Resize down to target size with high-quality filter
    img = img.resize((size, size), Image.LANCZOS)
    return img
