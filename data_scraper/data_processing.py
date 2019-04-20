import json
import re
from datetime import datetime

import pandas as pd

with open('dump_20190420.json', 'r') as fp:
    data = json.load(fp)

clean_estates = []
re_area = re.compile(r"Powierzchnia: <strong>")
re_chambers = re.compile(r"Liczba pokoi: <strong>")
re_market = re.compile(r"Rynek: <strong>")
re_building_type = re.compile(r"Rodzaj zabudowy: <strong>")
re_floor = re.compile(r"Piętro: <strong>")
re_building_floors = re.compile(r"Liczba pięter: <strong")
re_construction_year = re.compile(r"Rok budowy: <strong")
re_standard = re.compile(r"Stan wykończenia: <strong")

re_any_num = re.compile(r"(\d+,\d+) m|\d+ m")
re_number = re.compile(r"\d+")
re_inside_strong = re.compile(r"<strong>(\w+|\w+\s\w+)</strong>")


for record in data:
    # ceny
    price_clean = float(record["price"].strip(" zł").replace(" ", "").replace(",", "."))

    # powierzchnia
    area = list(filter(re_area.search, record["details"]))
    if (len(area) < 1) or (area is None):
        area_clean = None
    else:
        area_clean = (float(re_any_num.search(area[-1]).group().strip(" m").replace(",", ".")))

    # pokoje
    chamber = list(filter(re_chambers.search, record["details"]))
    if (len(chamber) < 1) or (chamber is None):
        chamber_clean = None
    else:
        chamber_clean = int(re_number.search(chamber[-1]).group())

    # rynek
    market = list(filter(re_market.search, record["details"]))
    if (len(market) < 1) or (market is None):
        market_clean = None
    else:
       market_clean = re_inside_strong.search(market[-1]).group(1)

    # typ budynku
    building = list(filter(re_building_type.search, record["details"]))
    if (len(building) < 1) or (building is None):
        building_clean = None
    else:
        building_clean = re_inside_strong.search(building[-1]).group(1)

    # piętro
    floor = list(filter(re_floor.search, record["details"]))
    if (len(floor) < 1) or (floor is None) or ("poddasze" in floor[0]):
        floor_clean = None
    else:
        if "&gt;" in floor[0]:
            floor_clean = 11
        elif "parter" in floor[0]:
            floor_clean = 0
        elif "suterena" in floor[0]:
            floor_clean = 0
        else:
            floor_clean = int(re_inside_strong.search(floor[-1]).group(1))

    # liczba pięter
    building_floors = list(filter(re_building_floors.search, record["details"]))
    if (len(building_floors) < 1) or (building_floors is None):
        building_floors_clean = None
    else:
        building_floors_clean = int(re_inside_strong.search(building_floors[-1]).group(1))

    # rok budowy
    construction_year = list(filter(re_construction_year.search, record["details"]))
    if (len(construction_year) < 1) or (construction_year is None):
        construction_year_clean = None
    else:
        construction_year_clean = int(re_inside_strong.search(construction_year[-1]).group(1))

    # standard mieszkania
    standard = list(filter(re_standard.search, record["details"]))
    if (len(standard) < 1) or (standard is None):
        standard_clean = None
    else:
        standard_clean = re_inside_strong.search(standard[-1]).group(1)


    # uzupełnianie słownika
    item = {"price": price_clean, "area": area_clean, "chamber": chamber_clean, "market": market_clean,
            "building": building_clean, "floor": floor_clean, "building_floors": building_floors_clean,
            "url": record["url"], "construction_year": construction_year_clean, "standard": standard_clean}
    clean_estates.append(item)

clean_df = pd.DataFrame(clean_estates)

clean_df.to_csv(f"data_clean_{datetime.now().strftime('%Y%m%d')}.csv", index=False)

print("Processing task finished")
