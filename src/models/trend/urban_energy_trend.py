import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns

# Load datasets
dietary_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"
urban_pop_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv"

dietary_data = pd.read_csv(dietary_path, encoding='ISO-8859-1')
urban_data = pd.read_csv(urban_pop_path, encoding='ISO-8859-1')
total_pop_data = urban_data[urban_data['Element'] == 'Total Population - Both sexes']

# Filter for 'Average dietary energy requirement' and 'Urban population'
dietary_data = dietary_data[dietary_data['Item'] == 'Average dietary energy requirement (kcal/cap/day)']
urban_data = urban_data[urban_data['Element'] == 'Urban population']

# Convert year columns to numeric and set index to 'Area' for both datasets
year_columns = [col for col in dietary_data.columns if col.startswith('Y') and len(col) == 5]
dietary_data[year_columns] = dietary_data[year_columns].apply(pd.to_numeric, errors='coerce')
dietary_data.set_index('Area', inplace=True)
total_pop_data.set_index('Area', inplace=True)
urban_data.set_index('Area', inplace=True)

merged_data_list = []

# Ensure only matching years and countries are merged
common_years = set(year_columns).intersection(urban_data.columns).intersection(total_pop_data.columns)
common_countries = list(set(dietary_data.index).intersection(urban_data.index).intersection(total_pop_data.index))

for year in common_years:
    # Convert the set to a list when using it as an indexer
    urban_percentage = (urban_data.loc[common_countries, year] / total_pop_data.loc[common_countries, year]) * 100
    temp_df = pd.DataFrame({
        'Area': common_countries,
        'Year': int(year[1:]),
        'AverageDietaryEnergy': dietary_data.loc[common_countries, year].values,
        'UrbanPopulationPercentage': urban_percentage.values
    })
    merged_data_list.append(temp_df)

merged_data = pd.concat(merged_data_list, ignore_index=True)

merged_data.dropna(inplace=True)
merged_data.drop_duplicates(inplace=True)

plt.figure(figsize=(15, 10))

# Generate a color palette, one color per country
palette = sns.color_palette("hsv", len(merged_data['Area'].unique()))
color_map = dict(zip(merged_data['Area'].unique(), palette))

# Loop through each country and perform regression
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]

    slope, intercept, r_value, p_value, std_err = linregress(country_data['Year'], country_data['AverageDietaryEnergy'])

    current_years = np.array(country_data['Year'])
    future_years = np.arange(current_years.max() + 1, current_years.max() + 11)  # Predicting next 10 years

    trendline_current = intercept + (slope * current_years)
    trendline_future = intercept + (slope * future_years)
    country_color = color_map[country]  # Use the unique color for the country

    # Plotting the data and the trendline for each country
    plt.scatter(country_data['Year'], country_data['AverageDietaryEnergy'], color=country_color, label=f'{country} Data')
    plt.plot(current_years, trendline_current, color=country_color, label=f'{country} Current Trend')
    plt.plot(future_years, trendline_future, '--', color=country_color, label=f'{country} Future Trend')

plt.title('Trend and Prediction of Average Dietary Energy Over Years by Country')
plt.xlabel('Year')
plt.ylabel('Average Dietary Energy (kcal/cap/day)')
plt.legend()
plt.grid(True)
plt.show()