import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv"  # Replace with your dataset file path
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Filter for 'Urban population'
urban_population_data = data[data['Element'] == 'Urban population']

# Convert year columns to numeric, replacing non-numeric values with NaN
for col in urban_population_data.columns:
    if col.startswith('Y'):
        urban_population_data[col] = pd.to_numeric(urban_population_data[col], errors='coerce')

# Plot
plt.figure(figsize=(15, 8))
for country in urban_population_data['Area'].unique():
    country_data = urban_population_data[urban_population_data['Area'] == country]
    year_columns = country_data.columns[country_data.columns.str.startswith('Y')]
    plt.plot(year_columns, country_data.iloc[0][year_columns], label=country)

plt.title('Urban Population Over the Years')
plt.xlabel('Year')
plt.ylabel('Urban Population (in thousands)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjusts the plot layout
plt.show()
