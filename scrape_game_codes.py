import requests
from bs4 import BeautifulSoup
import json

# Dictionary to store codes
codes = {
    'new': [],
    'used': []
}

# Save the dictionary to a JSON file
def save_codes():
    with open('codes.json', 'w') as file:
        json.dump(codes, file)

# Load the dictionary from a JSON file
def load_codes():
    global codes
    try:
        with open('codes.json', 'r') as file:
            data = json.load(file)
            if 'new' in data and 'used' in data:
                codes = data
            else:
                save_codes()  # Save default structure if keys are missing
    except (FileNotFoundError, json.JSONDecodeError):
        save_codes()

# Scrape codes from escapistmagazine.com
def scrape_escapistmagazine():
    url = 'https://www.escapistmagazine.com/solo-leveling-arise-codes/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    new_codes = []
    heading = soup.find('h3', {'id': 'h-solo-leveling-arise-codes-working'})
    if heading:
        ul = heading.find_next('ul', {'data-found-items': '10'})
        if ul:
            for li in ul.find_all('li'):
                strong_tag = li.find('strong')
                if strong_tag:
                    new_codes.append(strong_tag.get_text())

    return new_codes

# Scrape codes from thegamer.com
def scrape_thegamer():
    url = 'https://www.thegamer.com/solo-leveling-arise-codes-updated-daily/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    new_codes = []
    table = soup.select_one('div.table-container table')
    if table:
        rows = table.select('tbody tr')
        for row in rows:
            code_cell = row.select_one('td p strong')
            if code_cell:
                new_codes.append(code_cell.get_text())

    return new_codes

# Update the codes
def update_codes():
    global codes
    escapist_codes = scrape_escapistmagazine()
    gamer_codes = scrape_thegamer()

    new_codes = set(escapist_codes + gamer_codes)
    current_new_codes = set(codes['new'])
    current_used_codes = set(codes['used'])

    # Add new codes that are not already in the used or new list
    updated_new_codes = list((new_codes - current_new_codes - current_used_codes))
    if updated_new_codes:
        codes['new'].extend(updated_new_codes)
        save_codes()
        print("New codes found and updated.")
    else:
        print("No new codes found.")

    # Print the current new codes
    print("Current new codes:", codes['new'])

# Mark a code as used
def mark_code_as_used(code):
    if code in codes['new']:
        codes['new'].remove(code)
        codes['used'].append(code)
        save_codes()
        print(f"Code '{code}' marked as used.")
    else:
        print(f"Code '{code}' not found in new codes.")

# Load existing codes from file
load_codes()

# Run the update codes function for debugging
update_codes()

# Mark current codes as used
# used_codes = ['THANXTOGLOBALHUNTERS', 'NLHCSTREAM', 'Hunterpass1st', 'SOLOLEVELING_0508', 'WORLD1STLEVELUP', 'LETSGOKOREAGUILDS', 'THXSLVARISETHX', 'SOLODEVNOTE50', 'THXSLVARISE', 'NENEARISE', 'MOLLYMEILIN', 'Mollymeilin', 'SOLOLEVELINGSKR', 'WHOSNATIONALL3VEL', 'SOLODEVNOTE', 'STAYSHARP', 'SHARPSTREAM']
# for code in used_codes:
#     mark_code_as_used(code)

# Simple code to mark codes as used
# mark_code_as_used(code)