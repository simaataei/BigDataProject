def return_labels(dataset):
    classes = []
    family_map = {}
    for item in dataset:
        family = '.'.join(item.id.split('|')[-1].split('.')[0:3])
        if family not in family_map:
            family_map[family] = len(family_map)
        classes.append(family_map[family])
    return classes
