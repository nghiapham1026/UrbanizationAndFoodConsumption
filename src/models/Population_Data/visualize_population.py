import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"..\..\..\data\processed\Population_Data\Population_S_Asia_NOFLAG.csv"  # Update this to your dataset's path
data = pd.read_csv(file_path)

# Extracting years from the columns (assuming year columns start with 'Y')
years = [col for col in data.columns if col.startswith('Y')]

# Pivot the data to have years as columns and countries as rows
pivot_data = data.pivot_table(index='Area', values=years)

# Plotting
plt.figure(figsize=(15, 8))
for country in pivot_data.index:
    country_data = pivot_data.loc[country, :]
    plt.plot(years, country_data.values, label=country)

plt.title('Population Growth Over the Years')
plt.xlabel('Year')
plt.ylabel('Population (in thousands)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjust layout
plt.show()
