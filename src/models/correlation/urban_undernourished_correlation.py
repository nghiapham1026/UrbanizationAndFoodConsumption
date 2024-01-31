import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
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

# Extract data for urban population, total population, and number of undernourished
urban_population = extract_relevant_data(population_data, 'Urban population', None)
total_population = extract_relevant_data(population_data, 'Total Population - Both sexes', None)
undernourished = extract_relevant_data(dietary_data, None, 'Number of people undernourished (million) (3-year average)')

# Reshape the data for merging
urban_population_melted = urban_population.melt(id_vars='Area', var_name='Year', value_name='Urban Population')
total_population_melted = total_population.melt(id_vars='Area', var_name='Year', value_name='Total Population')
undernourished_melted = undernourished.melt(id_vars='Area', var_name='Year', value_name='Undernourished')

# Merge the datasets
merged_data = pd.merge(pd.merge(urban_population_melted, total_population_melted, on=['Area', 'Year']), undernourished_melted, on=['Area', 'Year'])

# Convert urban and total populations from thousands to absolute numbers and calculate percentages
merged_data['Urban Population'] = merged_data['Urban Population'] * 1e3  # Convert from thousands to absolute numbers
merged_data['Total Population'] = merged_data['Total Population'] * 1e3  # Convert from thousands to absolute numbers
merged_data['Undernourished'] = merged_data['Undernourished'] * 1e6  # Convert from million to absolute numbers

merged_data['Urban Population Percentage'] = (merged_data['Urban Population'] / merged_data['Total Population']) * 100
merged_data['Undernourished Percentage'] = (merged_data['Undernourished'] / merged_data['Total Population']) * 100

# Drop NaN values
merged_data.dropna(subset=['Urban Population Percentage', 'Undernourished Percentage'], inplace=True)

# Calculate Pearson correlation
correlation, p_value = pearsonr(merged_data['Urban Population Percentage'], merged_data['Undernourished Percentage'])
print(f'Pearson correlation: {correlation}, P-value: {p_value}')

# Plotting
plt.figure(figsize=(12, 8))
sns.scatterplot(x='Urban Population Percentage', y='Undernourished Percentage', hue='Area', data=merged_data)
plt.title('Urban Population Percentage vs Undernourished Percentage by Country')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Undernourished Percentage')
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
