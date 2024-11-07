import requests

BASE_URL = "https://trouverunlogement.lescrous.fr"
BASE_SEARCH_URL = f"{BASE_URL}/api/fr/search/37"
BASE_LINK_URL = f"{BASE_URL}/tools/37/accommodations/"

SEARCH_CITY_API_URL = f"{BASE_URL}/photon/api?q="

OCCUPATION_MODES = {
    "individuel": "alone",
    "colocation": "house_sharing",
    "couple": "couple"
}

def get_city_coord(param:dict) -> dict:
    """
    Get each cities coordinate [x1, y1, x2, y2]
    """
    cities_data = {}
    for city in param["villes"]:
        city_name = city["nom"].lower()
        cities_data[city_name] = []

        try:
            response = requests.get(
                SEARCH_CITY_API_URL+city["nom"],
                timeout=10
            )
            response.raise_for_status()

            if response.json():
                data = response.json()
                if data["features"]:
                    for city_data in data["features"]:
                        if "extent" not in city_data["properties"].keys():
                            continue

                        if city_data["properties"]["name"].lower() == city_name:
                            cities_data[city_name].append(city_data["properties"]["extent"])

        except requests.exceptions.Timeout:
            print(f"Timeout exceeded (get_city_coord) for city: {city_name}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed (get_city_coord) for city {city_name}: {e}")
    return cities_data

def params_converter(params:dict) -> dict:
    """
    Transform each cities in json param for CROUS request
    """
    cities_data = get_city_coord(params)

    modes_translated = [OCCUPATION_MODES[mode] for mode in params["modes"] if mode in OCCUPATION_MODES]

    for city, city_coords in cities_data.items():
        jsons_data = []
        for coord in city_coords:
            json_data = {
                'idTool': 37,
                'need_aggregation': True,
                'page': 1,
                'pageSize': 24,
                'sector': None,
                'occupationModes': modes_translated,
                'location': [
                    {
                        'lon': coord[0],
                        'lat': coord[1],
                    },
                    {
                        'lon': coord[2],
                        'lat': coord[3],
                    },
                ],
                'residence': None,
                'precision': 6,
                'equipment': [],
                'adaptedPmr': False,
                'toolMechanism': 'flow',
            }

            if params["prix"]["max"] != 0:
                json_data['price'] = {
                    'max': params["prix"]["max"]*100,
                }

            jsons_data.append(json_data)
        cities_data[city] = jsons_data
    return cities_data

def get_crous(params:dict) -> dict:
    """
    Make requests for each cities
    """
    cities_requests = params_converter(params)
    cities_results = {}

    for city, city_jsons in cities_requests.items():
        results = []
        for city_json in city_jsons:
            try:
                response = requests.post(
                    BASE_SEARCH_URL,
                    json=city_json,
                    timeout=10
                )
                response.raise_for_status()

                data = response.json()
                if len(data["results"]["items"])>0:
                    results.extend([BASE_LINK_URL+str(x["id"]) for x in data["results"]["items"]])

            except requests.exceptions.Timeout:
                print(f"Timeout exceeded (get_crous) for city: {city}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed (get_crous) for city {city}: {e}")
        cities_results[city.capitalize()] = results

    return cities_results
