import json, asyncio
import scrappers.Crous.crous as crous

params = {}
with open('parameters.json', 'r') as file:
    params = json.load(file)

print("Analyse de trouverunlogement.lescrous.fr...")
crousData = crous.get_crous(params)
print("Analyse de trouverunlogement.lescrous.fr fini!")

print("---------- RÉSULTATS ----------")
for city in crousData:
    print(f"{city} :")
    offers = crousData[city]
    for x in offers:
        print(f"    - {x}")
    print(f'\n{"-"*10}\n')