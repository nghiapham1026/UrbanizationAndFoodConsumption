import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv", encoding='ISO-8859-1')

# Filter for 'Number of adults under 5 years of age who are overweight'
overweight_adults_data = data[data['Item'] == 'Number of obese adults (18 years and older) (million)']

# Select only columns with year format 'Y2000', 'Y2001', etc.
year_columns = [col for col in overweight_adults_data.columns if col.startswith('Y') and len(col) == 5]

# Convert data to numeric, replacing non-numeric values with NaN
overweight_adults_data[year_columns] = overweight_adults_data[year_columns].apply(pd.to_numeric, errors='coerce')

# Plot
plt.figure(figsize=(10, 6))
for country in overweight_adults_data['Area'].unique():
    country_data = overweight_adults_data[overweight_adults_data['Area'] == country]
    plt.plot(country_data[year_columns].columns, country_data[year_columns].values.flatten(), label=country)

plt.title('Number of Overweight Adults Under 5 Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Adults (Millions)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()
