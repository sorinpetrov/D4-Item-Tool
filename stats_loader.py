import json

def load_best_stats(file_path='best_stats.json'):
    try:
        with open(file_path, 'r') as f:
            best_stats = json.load(f)
    except FileNotFoundError:
        best_stats = {}
    return best_stats

def normalize_item_type(item_type):
    item_type = item_type.lower().replace('-', ' ').replace('two', '2')
    normalized_types = {
        "1 handed axe": "1 Handed Axe", "one handed axe": "1 Handed Axe",
        "2 handed axe": "2 Handed Axe", "two handed axe": "2 Handed Axe",
        "1 handed sword": "1 Handed Sword", "one handed sword": "1 Handed Sword",
        "2 handed sword": "2 Handed Sword", "two handed sword": "2 Handed Sword",
        "1 handed mace": "1 Handed Mace", "one handed mace": "1 Handed Mace",
        "2 handed mace": "2 Handed Mace", "two handed mace": "2 Handed Mace",
        "1 handed scythe": "1 Handed Scythe", "one handed scythe": "1 Handed Scythe",
        "2 handed scythe": "2 Handed Scythe", "two handed scythe": "2 Handed Scythe",
        "dagger": "Dagger", "polearm": "Polearm", "wand": "Wand", "staff": "Staff",
        "bow": "Bow", "crossbow": "Crossbow", "focus": "Focus", "shield": "Shield",
        "helm": "Helm", "chest armor": "Chest Armor", "gloves": "Gloves",
        "pants": "Pants", "boots": "Boots", "necklace": "Necklace", "ring": "Ring"
    }
    return normalized_types.get(item_type, None)

def update_best_stats(file_path='best_stats.json'):
    best_stats = load_best_stats(file_path)
    
    while True:
        item_type = input("Enter the item type (or 'done' to finish): ").strip()
        if item_type.lower() == 'done':
            break
        
        normalized_item_type = normalize_item_type(item_type)
        if not normalized_item_type:
            print("Invalid item type. Please enter a valid item type.")
            continue
        
        best_stats[normalized_item_type] = {}

        for priority in range(1, 4):
            stats = input(f"Enter stats for priority {priority} (comma-separated, leave empty to skip): ").strip()
            if stats:
                best_stats[normalized_item_type][str(priority)] = [stat.strip() for stat in stats.split(',')]
        
        print(f"Updated stats for {normalized_item_type}: {best_stats[normalized_item_type]}")

    with open(file_path, 'w') as f:
        json.dump(best_stats, f, indent=4)
    print(f"Best stats updated and saved to {file_path}.")
