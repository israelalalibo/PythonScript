import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import calendar

# Enter the link to the CSV file containing the provided data
csv_link = "../ccf_monthly_data_backlog/current_CO2e_data.csv"

# Read CSV file into a DataFrame
df = pd.read_csv(csv_link, parse_dates=['Timestamp'])

# Plot trendlines for each cloud provider
plt.figure(figsize=(10, 6))

for column in df.columns[1:]:
    plt.plot(df['Timestamp'], df[column], marker='o', linestyle='-', label=column)

plt.title('CO2e Usage Trendlines by Cloud Provider')
plt.xlabel('Timestamp')
plt.ylabel('CO2e Usage (MTCO2e)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# path of the images folder for the HackCamp website
image_path = '../HackcampWebsite/Images/current_trendline.png'

# Get the current date and reduce it by one day, so that a report on sept 1, gives the month of August (for example)
current_date = datetime.now()
previous_day = current_date - timedelta(days=1)
previous_month = previous_day.month
previous_month_name = calendar.month_name[previous_month]
previous_year = previous_day.year

# path of the backlog folder
image_path_backlog = f'../ccf_monthly_data_backlog/CO2e_charts_backlog/{previous_month_name}_{previous_year}_CO2e_trendline.png'

# saves a copy of the image to the root level of Images folder for the website
plt.savefig(image_path)

# saves another copy of the image to the backlog folder containing historical data for the footprint data
plt.savefig(image_path_backlog)

print(f"Graph saved to '{image_path}'.")