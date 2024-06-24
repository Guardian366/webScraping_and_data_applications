import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import time

# Function to scrape property data from the website
def scrape_property_data():
    base_url = 'https://www.property.co.zw/property-for-sale'
    page = 1
    properties = []

    while True:
        url = f'{base_url}?page={page}'
        print(f"Scraping page: {page}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        listings = soup.select('div.result-cards > div.ResultCardItem')
        if not listings:
            print("No more listings found.")
            break  # No more listings found, exit the loop

        for listing in listings:
            property_id = listing.get('id')
            title = listing.select_one('h2 a').text.strip() if listing.select_one('h2 a') else 'N/A'
            location = listing.select_one('div.text-graypurpledark').text.strip() if listing.select_one('div.text-graypurpledark') else 'N/A'
            price = listing.select_one('div.result-price a').text.strip() if listing.select_one('div.result-price a') else 'N/A'
            size = listing.select_one('span.land-size').text.strip() if listing.select_one('span.land-size') else 'N/A'
            details = listing.select_one('div.ResultDescription').text.strip() if listing.select_one('div.ResultDescription') else 'N/A'
            date_posted = listing.select_one('div.result-date').text.strip() if listing.select_one('div.result-date') else 'N/A'

            properties.append({
                'property_id': property_id,
                'title': title,
                'location': location,
                'price': price,
                'size': size,
                'details': details,
                'date_posted': date_posted,
                'date_scraped': datetime.date.today()
            })
        
        page += 1
        time.sleep(1)  # Add a delay to prevent overwhelming the server

    return properties

# Function to save the property data to an Excel file
def save_to_excel(new_data):
    file_path = 'property_data.xlsx'
    changes_file_path = 'property_data_changes.xlsx'

    # Check if the Excel file already exists
    if os.path.exists(file_path):
        # Load the existing data
        existing_data = pd.read_excel(file_path)
        existing_ids = set(existing_data['property_id'].values)

        # DataFrames to store changes
        updated_data = []
        changes_data = []

        for new_prop in new_data:
            if new_prop['property_id'] in existing_ids:
                # Check for changes
                existing_prop = existing_data.loc[existing_data['property_id'] == new_prop['property_id']].iloc[0]
                changes = {}
                for key in ['title', 'location', 'price', 'size', 'details', 'date_posted']:
                    if new_prop[key] != existing_prop[key]:
                        changes[key] = (existing_prop[key], new_prop[key])

                if changes:
                    new_prop['date_updated'] = datetime.date.today()
                    changes['property_id'] = new_prop['property_id']
                    changes['date_updated'] = new_prop['date_updated']
                    changes_data.append(changes)
                    updated_data.append(new_prop)
                else:
                    updated_data.append(existing_prop)
            else:
                updated_data.append(new_prop)

        updated_df = pd.DataFrame(updated_data)
        changes_df = pd.DataFrame(changes_data)

        # Save the updated data to the Excel file
        updated_df.to_excel(file_path, index=False)

        # Save changes to a separate file
        if os.path.exists(changes_file_path):
            changes_existing_df = pd.read_excel(changes_file_path)
            combined_changes_df = pd.concat([changes_existing_df, changes_df], ignore_index=True)
        else:
            combined_changes_df = changes_df

        combined_changes_df.to_excel(changes_file_path, index=False)
    else:
        # Create a new DataFrame
        df = pd.DataFrame(new_data)
        df.to_excel(file_path, index=False)

    print(f"Data saved to {file_path}")

# Main function to execute the scraping and saving process
def main():
    property_data = scrape_property_data()
    if property_data:
        print(f"Scraped {len(property_data)} properties:")
        for prop in property_data:
            print(prop)
        save_to_excel(property_data)
    else:
        print("No properties scraped.")

if __name__ == '__main__':
    main()
