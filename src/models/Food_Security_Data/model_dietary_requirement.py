import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Filter for 'Average dietary energy requirement'
dietary_requirement_data = data[data['Item'] == 'Average dietary energy requirement (kcal/cap/day)']

# Convert all year columns (in the format 'Y2000') to numeric, replacing non-numeric values with NaN
year_columns = [col for col in dietary_requirement_data.columns if col.startswith('Y') and len(col) == 5]
for col in year_columns:
    dietary_requirement_data[col] = pd.to_numeric(dietary_requirement_data[col], errors='coerce')

# Plot
plt.figure(figsize=(10, 6))
for country in dietary_requirement_data['Area'].unique():
    country_data = dietary_requirement_data[dietary_requirement_data['Area'] == country]
    plt.plot(country_data[year_columns].columns, country_data[year_columns].values.flatten(), label=country)

plt.title('Average Dietary Energy Requirement Over the Years')
plt.xlabel('Year')
plt.ylabel('Energy Requirement (kcal/cap/day)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjusts the plot layout
plt.show()
