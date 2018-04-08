import re
import json
import string
from functools import reduce
from collections import Counter

with open("data/skill_dictionary") as reader:
    skill_dictionary = json.load(reader)

# for k in skill_dictionary:
#     print(k, skill_dictionary[k])

all_skill_list = []
for k in skill_dictionary:
    for text in skill_dictionary[k]:
        regex = re.compile('[%s]' % re.escape("(),:абвгдеёжзиёклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"))
        clear_text = regex.sub('', text)
        all_skill_list += clear_text.strip().split()

# print(all_skill_list)

counter = Counter(all_skill_list)
print(counter)
res_skill_dictionary = {}
for k in skill_dictionary:
    res_skill_dictionary[k] = {}
    for text in skill_dictionary[k]:
        regex = re.compile('[%s]' % re.escape("(),:абвгдеёжзиёклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"))
        clear_text = regex.sub('', text).strip()
        words = clear_text.split()
        res_skill_dictionary[k][clear_text] = [clear_text]
        for word in words:
            if counter[word] < 2 and word not in res_skill_dictionary[k][clear_text] and not word.isdigit() and word != "":
                res_skill_dictionary[k][clear_text].append(word)

# additional changes
del res_skill_dictionary["1"]["1-"]
del res_skill_dictionary["1"]["1"]
res_skill_dictionary["1"]["1С"] = ["1С"]
res_skill_dictionary["1"]["1С-Битрикс"] = ["1С-Битрикс"]
res_skill_dictionary["1"]["1С:Деньги"] = ["1С:Деньги"]
res_skill_dictionary["1"]["1С:Документооборот"] = ["1С:Документооборот"]
res_skill_dictionary["1"]["1С:Предприятие"] = ["1С:Предприятие"]

del res_skill_dictionary["C"]["C Sharp"]

res_skill_dictionary["C"]["C#"] = ["C#", "C Sharp"]

del res_skill_dictionary["F"]["F Sharp"]

res_skill_dictionary["F"]["F#"] = ["F#", "F Sharp"]

res_skill_dictionary["C"]["C"] = ["C", "Си"]

res_skill_dictionary["."][".NET Framework"].append(".NET")

res_skill_dictionary["S"]["Spring Framework"].append("Spring")

print(res_skill_dictionary)


with open("counter", "w") as writer:
    writer.write(json.dumps(counter))

with open("res_skill_dictionary", "w") as writer:
    writer.write(json.dumps(res_skill_dictionary))

