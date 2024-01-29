import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

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
carbohydrate_intake = extract_relevant_data(dietary_data, None, 'Share of dietary energy supply derived from cereals, roots and tubers (kcal/cap/day) (3-year average)')

urban_population_melted = urban_population.melt(id_vars='Area', var_name='Year', value_name='Urban Population')
total_population_melted = total_population.melt(id_vars='Area', var_name='Year', value_name='Total Population')
carbohydrate_intake_melted = carbohydrate_intake.melt(id_vars='Area', var_name='Year', value_name='Carbohydrate Intake')

merged_data = pd.merge(pd.merge(urban_population_melted, total_population_melted, on=['Area', 'Year']), carbohydrate_intake_melted, on=['Area', 'Year'])

# Convert to absolute numbers and calculate percentages
merged_data['Urban Population'] = merged_data['Urban Population'] * 1e3
merged_data['Total Population'] = merged_data['Total Population'] * 1e3
merged_data['Urban Population Percentage'] = (merged_data['Urban Population'] / merged_data['Total Population']) * 100

merged_data.dropna(subset=['Urban Population Percentage', 'Carbohydrate Intake'], inplace=True)

plt.figure(figsize=(15, 10))

# Loop through each country and calculate trend
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]
    if len(country_data) > 1:
        # Calculate trend for each country
        slope, intercept, r_value, p_value, std_err = linregress(country_data['Urban Population Percentage'], country_data['Carbohydrate Intake'])

        # Define the current and future urban population percentage
        current_urban_percentage = np.array(country_data['Urban Population Percentage'])
        future_urban_percentage = np.linspace(current_urban_percentage.max(), current_urban_percentage.max() + 5, 5)  # Assume a 5% increase for illustration

        # Calculate the trendline for current and future
        trendline_current = intercept + slope * current_urban_percentage
        trendline_future = intercept + slope * future_urban_percentage

        # Plotting each country's data and trend line
        plt.scatter(country_data['Urban Population Percentage'], country_data['Carbohydrate Intake'], label=f'{country} Data')
        plt.plot(current_urban_percentage, trendline_current, label=f'{country} Current Trend')
        plt.plot(future_urban_percentage, trendline_future, '--', label=f'{country} Future Trend')

plt.title('Trend and Prediction of Urban Population Percentage vs Carbohydrate Intake by Country')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Carbohydrate Intake (kcal/cap/day)')
plt.legend()
plt.grid(True)
plt.show()