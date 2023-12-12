import requests
import csv
from collections import defaultdict
from datetime import datetime, timedelta
import calendar
import os


def process_data(data):
    # Process data to aggregate CO2e usage by date and cloudProvider
    co2e_by_date_provider = defaultdict(lambda: defaultdict(float))

    for entry in data:
        timestamp = entry['timestamp']
        service_estimates = entry['serviceEstimates']

        for service in service_estimates:
            cloud_provider = service['cloudProvider']
            co2e = service['co2e']
            co2e_by_date_provider[timestamp][cloud_provider] += co2e

    return co2e_by_date_provider


def generate_csv(data):
    # getting date information to ensure that each monthly file name is unique.
    current_date = datetime.now()
    previous_day = current_date - timedelta(days=1)
    previous_month = previous_day.month
    previous_month_name = calendar.month_name[previous_month]
    previous_year = previous_day.year

    # Generate CSV file from processed data
    csv_filename = f'../ccf_monthly_data_backlog/CO2e_data_backlog/{previous_month_name}_{previous_year}_CO2e_data.csv'

    if os.path.exists(csv_filename):
        csv_filename = f'../ccf_monthly_data_backlog/current_CO2e_data.csv'
    else:
        pass

    with open(csv_filename, mode='w', newline='') as csv_file:
        fieldnames = ['Timestamp'] + list(data[next(iter(data))].keys())  # Get cloudProviders as headers
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for timestamp, providers in data.items():
            row = {'Timestamp': timestamp}
            row.update(providers)
            writer.writerow(row)

    print(f"CSV file '{csv_filename}' created successfully.")


# Prompt for the URL containing the JSON data
data_url = "http://localhost:4000/footprint"

try:
    response = requests.get(data_url)
    if response.status_code == 200:
        data = response.json()
        processed_data = process_data(data)
        generate_csv(processed_data)
        generate_csv(processed_data)
    else:
        print(f"Failed to fetch data from {data_url}. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
