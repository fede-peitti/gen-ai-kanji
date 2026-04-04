import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image
import io


def render_kanji_svg_to_png(kanji_element, size=128):
    """
    Convert a KanjiVG <kanji> element to a grayscale PNG PIL image.
    Ensures all strokes are black and fill is none.
    """
    # Deep copy element to avoid modifying original
    kanji_copy = ET.fromstring(ET.tostring(kanji_element))

    # Force all <path> elements to have black stroke, no fill
    for path in kanji_copy.findall(".//path"):
        path.attrib["stroke"] = "#000000"
        path.attrib["fill"] = "none"
        path.attrib["stroke-width"] = "2"  # optional: makes lines thicker

    # Convert element back to string
    kanji_svg_content = ET.tostring(kanji_copy, encoding="unicode")

    # Wrap in <svg> root
    svg_data = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="109" height="109" viewBox="0 0 109 109">
        {kanji_svg_content}
    </svg>
    """

    # Render SVG → PNG bytes
    png_bytes = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))

    # Open with PIL, grayscale, resize
    img = Image.open(io.BytesIO(png_bytes)).convert("L")
    img = img.resize((size, size))
    return img
