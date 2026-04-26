def clean_meanings(meanings, max_terms=3):
    cleaned = []
    for m in meanings:
        m = m.lower().strip()

        if not m:
            continue

        if "(" in m:
            m = m.split("(")[0].strip()

        if "radical" in m:
            continue

        parts = m.split()
        if not parts:
            continue
        m = parts[0]

        if m in ["a", "an", "the"]:
            continue

        if m not in cleaned:
            cleaned.append(m)

    return cleaned[:max_terms]


def build_dataset(pairs, limit=None):
    dataset = []

    subset = pairs if limit is None else pairs[:limit]

    for pair in subset:
        char = pair["char"]
        meanings = clean_meanings(pair["meanings"])
        text = " ".join(meanings)

        dataset.append({"image": f"images/{char}.png", "text": text})

    return dataset
