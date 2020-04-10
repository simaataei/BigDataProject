# Number of long sequences removed from each Family
import json
import matplotlib.pyplot as plt

with open('family_deleted_long_sequences.txt') as json_file:
    data = json.load(json_file)

sorted_dict = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
selected = {}
i = 0
for item in sorted_dict:
    selected[item] = sorted_dict[item]
    i += 1
    if i == 10:
        break

plt.bar(range(len(selected)), list(selected.values()), align='center')
plt.xticks(range(len(selected)), list(selected.keys()))
plt.show()

a = 1
