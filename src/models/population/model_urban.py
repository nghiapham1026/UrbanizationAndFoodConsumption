import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
population_data_path = r"..\..\..\data\processed\Population_Data\Population_S_Asia_NOFLAG.csv"

population_data = urban_population_data = pd.read_csv(population_data_path, encoding='ISO-8859-1')

# Extract data for total and urban populations
total_population = population_data[population_data['Element'] == 'Total Population - Both sexes']
urban_population = population_data[population_data['Element'] == 'Urban population']

# Convert year columns to numeric and calculate the urban population percentage
years = [col for col in total_population.columns if col.startswith('Y')]
urban_percentages = pd.DataFrame(index=total_population['Area'])

for year in years:
    urban_population_year = urban_population.set_index('Area')[year]
    total_population_year = total_population.set_index('Area')[year]
    urban_percentages[year] = (urban_population_year / total_population_year) * 100

# Plotting
plt.figure(figsize=(15, 8))
for country in urban_percentages.index:
    plt.plot(years, urban_percentages.loc[country], label=country)

plt.title('Urban Population Percentage Over the Years')
plt.xlabel('Year')
plt.ylabel('Urban Population Percentage')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
