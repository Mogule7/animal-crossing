from collections import Counter

def crafting_list():
    crafting = []
    safe_word = 'DONE'
    while True:
        question = input('Type furniture to be crafted (submit "Done" when finished): ').lower()
        if question.upper() == safe_word:
            break
        else:
            crafting.append(question)
    return crafting

def get_combined_materials(craftable, crafting):
    materials_dict = {}
    name_counter = Counter(crafting)

    for item in craftable:
        name = item['name']
        count = name_counter[name]
        if count > 0:
            materials = item['materials']
            for material, quantity in materials.items():
                materials_dict[material] = materials_dict.get(material, 0) + count * quantity
            name_counter[name] = 0

    return materials_dict