import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import seaborn as sns

# Load the datasets
population_data_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations_3_year.csv"
dietary_data_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"

population_data = pd.read_csv(population_data_path, encoding='ISO-8859-1')
dietary_data = pd.read_csv(dietary_data_path, encoding='ISO-8859-1')

# Extract relevant columns including 'Area'
def extract_relevant_data(df, element, item):
    interval_columns = [col for col in df.columns if 'Y' in col and len(col) == 9]
    return df[df['Element'] == element][['Area'] + interval_columns] if element else df[df['Item'] == item][['Area'] + interval_columns]

# Extract and reshape data
urban_population = extract_relevant_data(population_data, 'Urban population', None)
total_population = extract_relevant_data(population_data, 'Total Population - Both sexes', None)
undernourished = extract_relevant_data(dietary_data, None, 'Number of people undernourished (million) (3-year average)')

urban_population_melted = urban_population.melt(id_vars='Area', var_name='Year', value_name='Urban Population')
total_population_melted = total_population.melt(id_vars='Area', var_name='Year', value_name='Total Population')
undernourished_melted = undernourished.melt(id_vars='Area', var_name='Year', value_name='Undernourished')

merged_data = pd.merge(pd.merge(urban_population_melted, total_population_melted, on=['Area', 'Year']), undernourished_melted, on=['Area', 'Year'])

# Convert to absolute numbers and calculate percentages
merged_data['Urban Population'] = merged_data['Urban Population'] * 1e3
merged_data['Total Population'] = merged_data['Total Population'] * 1e3
merged_data['Undernourished'] = merged_data['Undernourished'] * 1e6

merged_data['Urban Population Percentage'] = (merged_data['Urban Population'] / merged_data['Total Population']) * 100
merged_data['Undernourished Percentage'] = (merged_data['Undernourished'] / merged_data['Total Population']) * 100

merged_data.dropna(subset=['Urban Population Percentage', 'Undernourished Percentage'], inplace=True)

plt.figure(figsize=(15, 10))

# Generate a color palette, one color per country
palette = sns.color_palette("hsv", len(merged_data['Area'].unique()))
color_map = dict(zip(merged_data['Area'].unique(), palette))

# Loop through each country and calculate trend
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]
    if len(country_data) > 1:
        # Calculate trend for each country
        slope, intercept, r_value, p_value, std_err = linregress(country_data['Urban Population Percentage'], country_data['Undernourished Percentage'])

        # Define current and future urban population percentage range
        current_urban_perc = np.array(country_data['Urban Population Percentage'])
        future_urban_perc = np.linspace(current_urban_perc.max(), current_urban_perc.max() + 5, 5)  # Extend 5% more

        # Calculate trendline for current and future range
        trendline_current = intercept + slope * current_urban_perc
        trendline_future = intercept + slope * future_urban_perc
        country_color = color_map[country]  # Use the unique color for the country

        # Plotting each country's data and trend line
        plt.scatter(country_data['Urban Population Percentage'], country_data['Undernourished Percentage'], color=country_color, label=f'{country} Data')
        plt.plot(current_urban_perc, trendline_current, color=country_color, label=f'{country} Current Trend')
        plt.plot(future_urban_perc, trendline_future, '--', color=country_color, label=f'{country} Future Trend')

plt.title('Current and Future Trend in Urban Population Percentage vs Undernourished Percentage by Country')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Undernourished Percentage')
plt.legend()
plt.grid(True)
plt.show()