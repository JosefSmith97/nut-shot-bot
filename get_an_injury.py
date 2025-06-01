import csv, requests, sys

from numpy import random
from pathlib import Path

def load_csv():
    with open('injuries.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dict_list = list(reader)
    return dict_list

def ingest_data(save):
    offset = 0
    injuries = []
    record_total = (requests.get(f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-data-on-injuries/records?where=narrative_1%20IS%20NOT%20NULL%20AND%20sex_code%20%3D%201%20AND%20body_part_code%20%3D%2038&limit=100")).json()["total_count"]

    while True:
        if len(injuries) == record_total:
            if save is True:
                with open('injuries.csv', 'w', newline='') as csvfile:
                    fieldnames = [key for key in injuries[0].keys()]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(injuries)
                print(f"'injuries.csv' created")
            break

        response = requests.get(f"https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-data-on-injuries/records?where=narrative_1%20IS%20NOT%20NULL%20AND%20sex_code%20%3D%201%20AND%20body_part_code%20%3D%2038&order_by=treatment_date%20DESC&limit=100&offset={offset}")
        print(f"Response with offset {offset}")
        response_json = response.json()

        for record in response_json["results"]:
            injury = { 
                "injury_description" : record["narrative_1"],
                "further_description": record["narrative_2"],
                "treatment_date": record["treatment_date"]
            }
            injuries.append(injury)
        print(f"Finished getting {offset} genital injuries")
        offset += 100
    print(f"Finished getting {len(injuries)} genital injuries")
    return injuries

if Path("injuries.csv").exists():
    print("Loading from pre-existing csv")
    injuries = load_csv()
else:
    print("Would you like to save this data as a csv to avoid loading next time? Yes or No")
    save_input = input()
    if save_input.lower() == "yes":
        save = True
        print("Creating csv")
    else:
        save = False
        print("Not creating csv")

    injuries = ingest_data(save)

while True:
    print("Would you like to see a random genital injury? Anything other than 'Yes' will exit")
    user_input = input()
    if user_input.lower() == "yes":
        random_number = random.randint(0, 6140)
        print(f"\nGetting injury number {random_number}...\n")
        injury = injuries[random_number]
        if injury.get("further_description"):
            full_description = injury["injury_description"] + injury["further_description"]
        else:
            full_description = injury["injury_description"]
        print("********************")
        print(f"Description:\n\n{full_description}\n")
        print(f"Date: {injury["treatment_date"]}")
        print("********************\n")
    else:
        sys.exit()