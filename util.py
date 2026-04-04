import xml.etree.ElementTree as ET


def build_usable_pairs(kanji_dict, kanjivg_root):
    usable_pairs = []
    for kanji in kanjivg_root:
        kanji_id = kanji.attrib.get("id", "")
        char = kanjivg_id_to_char(kanji_id)
        if char is None:
            continue
        if char in kanji_dict:
            usable_pairs.append(
                {
                    "char": char,
                    "meanings": kanji_dict[char],
                    "kanjivg_element": kanji,  # keep element for SVG later
                }
            )
    return usable_pairs


def kanjivg_id_to_char(kanji_id: str):
    """
    Convert a KanjiVG id like 'kvg:kanji_4e00' to the actual kanji character.
    Returns None if invalid.
    """
    if "kanji_" not in kanji_id:
        return None
    code = kanji_id.split("kanji_")[1]
    try:
        return chr(int(code, 16))
    except ValueError:
        return None


def load_kanjidic2(filename="kanjidic2.xml"):
    tree = ET.parse(filename)
    root = tree.getroot()
    kanji_dict = {}

    for char in root.findall("character"):
        literal = char.find("literal").text
        meanings = []
        for rmgroup in char.findall(".//rmgroup"):
            for meaning in rmgroup.findall("meaning"):
                if meaning.get("m_lang") is None:
                    meanings.append(meaning.text)
        if meanings:
            kanji_dict[literal] = meanings
    return kanji_dict


def load_kanjivg(filename="kanjivg.xml"):
    tree = ET.parse(filename)
    return tree.getroot()
