import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the datasets
population_data_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations_3_year.csv"
dietary_data_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"

population_data = pd.read_csv(population_data_path, encoding='ISO-8859-1')
dietary_data = pd.read_csv(dietary_data_path, encoding='ISO-8859-1')

# Define a function to extract the 3-year interval columns
def extract_3_year_intervals(df):
    interval_columns = [col for col in df.columns if 'Y20' in col and len(col) == 9]  # Adjusted to match the column format 'Yyyyyyyyy'
    return df[interval_columns]

# Extract the 3-year interval data for urban population and protein intake
urban_population = extract_3_year_intervals(population_data[population_data['Element'] == 'Urban population'])
protein_intake = extract_3_year_intervals(dietary_data[dietary_data['Item'] == 'Share of dietary energy supply derived from cereals, roots and tubers (kcal/cap/day) (3-year average)'])

# Ensure both datasets have the same intervals
common_intervals = urban_population.columns.intersection(protein_intake.columns)
urban_population = urban_population[common_intervals].mean(axis=0)
protein_intake = protein_intake[common_intervals].mean(axis=0)

# Drop NaN values from both series to ensure equal length
urban_population = urban_population.dropna()
protein_intake = protein_intake.dropna()

# Ensure the indexes are aligned after dropping NaNs
common_indexes = urban_population.index.intersection(protein_intake.index)
urban_population = urban_population[common_indexes]
protein_intake = protein_intake[common_indexes]

print(urban_population)
print(protein_intake)

# Calculate the Pearson correlation
correlation, p_value = pearsonr(urban_population, protein_intake)
print(f'Pearson correlation: {correlation}, P-value: {p_value}')