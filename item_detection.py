import re

item_keywords = {
    "One Handed Axe": ["1 Handed Axe", "One-Handed Axe"],
    "Two Handed Axe": ["2 Handed Axe", "Two-Handed Axe"],
    "One Handed Sword": ["1 Handed Sword", "One-Handed Sword"],
    "Two Handed Sword": ["2 Handed Sword", "Two-Handed Sword"],
    "One Handed Mace": ["1 Handed Mace", "One-Handed Mace"],
    "Two Handed Mace": ["2 Handed Mace", "Two-Handed Mace"],
    "One Handed Scythe": ["1 Handed Scythe", "One-Handed Scythe"],
    "Two Handed Scythe": ["2 Handed Scythe", "Two-Handed Scythe"],
    "Dagger": ["Dagger"],
    "Polearm": ["Polearm"],
    "Wand": ["Wand"],
    "Staff": ["Staff"],
    "Bow": ["Bow"],
    "Crossbow": ["Crossbow"],
    "Focus": ["Focus"],
    "Shield": ["Shield"],
    "Helm": ["Helm"],
    "Chest Armor": ["Chest Armor"],
    "Gloves": ["Gloves"],
    "Pants": ["Pants"],
    "Boots": ["Boots"],
    "Amulet": ["Amulet"],
    "Ring": ["Ring"]
}

def detect_item_type(cleaned_extracted_text):
    print(f"Cleaned Extracted Text for Item Detection: {cleaned_extracted_text}")
    for item_type, keywords in item_keywords.items():
        for keyword in keywords:
            if keyword.lower() in cleaned_extracted_text:
                print(f"Match found: {keyword.lower()} in {cleaned_extracted_text}")
                return item_type
    return "Unknown"
