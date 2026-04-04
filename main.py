from util import load_kanjidic2, load_kanjivg, build_usable_pairs
from render import render_kanji_svg_to_png

kanji_dict = load_kanjidic2()
print("Total kanji in KANJIDIC2:", len(kanji_dict))

kanjivg_root = load_kanjivg()
usable_pairs = build_usable_pairs(kanji_dict, kanjivg_root)
print("Total usable pairs:", len(usable_pairs))
print("Sample:", usable_pairs[0])

# Render first kanji
first_pair = usable_pairs[0]
img = render_kanji_svg_to_png(first_pair["kanjivg_element"], size=128)

# Save or display
img.save(f"images/{first_pair['char']}.png")
img.show()
