# CROUS Logement

Utilise l'API du CROUS pour récupérer les logements disponibles en fonction des filtres établis.

# INSTALLATION

- **1** - Clonez le repo : `git clone https://github.com/Aube33/crous-logement-python.git`.
- **2** - Accédez au dossier téléchargé.
- **3** - Paramétrez les filtres via `parameters.json` ([voir configuration](#configuration)).
- **4** - Lancez le programme via `python main.py`.
- **5** - Obtention des résultats, lorsque les résultats sont vides c'est qu'il n y a aucun logement actuellement disponible.
<a name="configuration"></a>
# CONFIGURATION

Toute la configuration ce fait dans le fichier `parameters.json`.
Il est possible de configurer les filtres suivant:

- **modes** : Type de logement souhaité (individuel, colocation, couple)
- **villes** : Ville(s) où chercher les logements
- **prix** : Définir un prix minimum et maximum

## Exemple de configuration:
Ici les filtres permettent de chercher les logements disponibles de type **inviduel** ou **couple**, situés à **Nantes** ou **Grenoble**, avec un loyer entre **100** et **350€**
``` json
{
    "modes": ["individuel", "couple"],
    "villes":
    [
        {
            "nom": "Nantes"
        },
        {
            "nom": "Grenoble"
        }
    ],
    "prix": {
        "min": 100,
        "max": 350
    }
}
```
- Les modes possibles sont `"individuel", "couple", "colocation"`
- Un filtre de prix max à 0 permet d'ignorer le prix