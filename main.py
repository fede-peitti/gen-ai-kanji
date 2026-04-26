import os
import json
from util import load_kanjidic2, load_kanjivg, build_usable_pairs
from render import render_kanji_svg_to_png
from dataset import build_dataset

BATCH_SIZE = None  # Set to None to process all, or specify a number for testing
IMAGE_SIZE = 256


def render_images(pairs, limit=None):
    os.makedirs("images", exist_ok=True)

    subset = pairs if limit is None else pairs[:limit]

    for pair in subset:
        char = pair["char"]
        kanji_elem = pair["kanjivg_element"]

        img = render_kanji_svg_to_png(kanji_elem, IMAGE_SIZE)
        img.save(f"images/{char}.png")

    print(f"Rendered {len(subset)} images")


# Load data
kanji_dict = load_kanjidic2()
print("Total kanji:", len(kanji_dict))

kanjivg_root = load_kanjivg()
usable_pairs = build_usable_pairs(kanji_dict, kanjivg_root)
print("Usable pairs:", len(usable_pairs))

# Render images
render_images(usable_pairs, limit=BATCH_SIZE)

# Build dataset
dataset = build_dataset(usable_pairs, limit=BATCH_SIZE)

print("\nSample:")
for item in dataset[:5]:
    print(item)

# Save dataset
with open("dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Saved dataset.json")
