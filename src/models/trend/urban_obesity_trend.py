import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Load datasets
obesity_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"
urban_pop_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv"

obesity_data = pd.read_csv(obesity_path, encoding='ISO-8859-1')
urban_data = pd.read_csv(urban_pop_path, encoding='ISO-8859-1')
total_pop_data = urban_data[urban_data['Element'] == 'Total Population - Both sexes']

# Filter for 'Number of obese adults (18 years and older) (million)' and 'Urban population'
obesity_data = obesity_data[obesity_data['Item'] == 'Number of obese adults (18 years and older) (million)']
urban_data = urban_data[urban_data['Element'] == 'Urban population']

# Convert year columns to numeric and set index to 'Area' for both datasets
year_columns = [col for col in obesity_data.columns if col.startswith('Y') and len(col) == 5]
obesity_data[year_columns] = obesity_data[year_columns].apply(pd.to_numeric, errors='coerce')
obesity_data.set_index('Area', inplace=True)
total_pop_data.set_index('Area', inplace=True)
urban_data.set_index('Area', inplace=True)

merged_data_list = []

# Ensure only matching years and countries are merged
common_years = set(year_columns).intersection(urban_data.columns).intersection(total_pop_data.columns)
common_countries = list(set(obesity_data.index).intersection(urban_data.index).intersection(total_pop_data.index))

for year in common_years:
    obesity_percentage = (obesity_data.loc[common_countries, year] / total_pop_data.loc[common_countries, year]) * 100
    urban_percentage = (urban_data.loc[common_countries, year] / total_pop_data.loc[common_countries, year]) * 100
    temp_df = pd.DataFrame({
        'Area': common_countries,
        'Year': int(year[1:]),
        'ObesityPercentage': obesity_percentage.values,
        'UrbanPopulationPercentage': urban_percentage.values
    })
    merged_data_list.append(temp_df)

merged_data = pd.concat(merged_data_list, ignore_index=True)

merged_data.dropna(inplace=True)
merged_data.drop_duplicates(inplace=True)

plt.figure(figsize=(10, 8))

# Loop through each country and perform regression
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]

    # Perform linear regression for each country
    slope, intercept, r_value, p_value, std_err = linregress(country_data['UrbanPopulationPercentage'], country_data['ObesityPercentage'])

    # Define the current and future urban population percentage range
    current_urban_perc = np.array(country_data['UrbanPopulationPercentage'])
    future_urban_perc = np.linspace(current_urban_perc.max(), current_urban_perc.max() + 5, 5)  # Assume a 5% increase for illustration

    # Calculate the trendline for current and future
    trendline_current = intercept + slope * current_urban_perc
    trendline_future = intercept + slope * future_urban_perc

    # Plotting each country's data and trend line
    plt.scatter(country_data['UrbanPopulationPercentage'], country_data['ObesityPercentage'], label=f'{country} Data')
    plt.plot(current_urban_perc, trendline_current, label=f'{country} Current Trend')
    plt.plot(future_urban_perc, trendline_future, '--', label=f'{country} Future Trend')

plt.title('Current and Future Trend in Urban Population Percentage vs Obesity Percentage')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Obesity Percentage')
plt.legend()
plt.grid(True)
plt.show()