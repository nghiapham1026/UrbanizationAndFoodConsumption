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

# Define a function to extract the 3-year interval columns
def extract_3_year_intervals(df):
    interval_columns = [col for col in df.columns if 'Y' in col and len(col) == 9]  # Adjusted to match the column format 'Yyyyyyyyy'
    return df[interval_columns]

# Extract the 3-year interval data for urban population and fat intake
urban_population = extract_3_year_intervals(population_data[population_data['Element'] == 'Urban population'])
fat_intake = extract_3_year_intervals(dietary_data[dietary_data['Item'] == 'Average fat supply (g/cap/day) (3-year average)'])

# Ensure both datasets have the same intervals
common_intervals = urban_population.columns.intersection(fat_intake.columns)
urban_population = urban_population[common_intervals].mean(axis=0)
fat_intake = fat_intake[common_intervals].mean(axis=0)

# Drop NaN values from both series to ensure equal length
urban_population = urban_population.dropna()
fat_intake = fat_intake.dropna()

# Ensure the indexes are aligned after dropping NaNs
common_indexes = urban_population.index.intersection(fat_intake.index)
urban_population = urban_population[common_indexes]
fat_intake = fat_intake[common_indexes]

# Create a DataFrame for plotting
plot_data = pd.DataFrame({
    'Urban Population': urban_population,
    'Fat Intake': fat_intake
})

# Calculate the Pearson correlation
correlation, p_value = pearsonr(plot_data['Urban Population'], plot_data['Fat Intake'])
print(f'Pearson correlation: {correlation}, P-value: {p_value}')

# Plotting
sns.regplot(x='Urban Population', y='Fat Intake', data=plot_data)
plt.title('Urban Population vs Fat Intake')
plt.xlabel('Urban Population (in thousands)')
plt.ylabel('Fat Intake (kcal/cap/day)')
plt.show()
