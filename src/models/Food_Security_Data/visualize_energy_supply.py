import pandas as pd
import matplotlib.pyplot as plt

# Assuming 'data' is your DataFrame after loading the CSV
file_path = r"..\..\..\data\processed\Food_Security_Data\Energy_Supply_S_Asia_NOFLAG.csv"  # Update this to your dataset's path
data = pd.read_csv(file_path)

# Filter for Average Dietary Energy Supply Adequacy
adequacy_data = data[data['Item'] == 'Average dietary energy supply adequacy (percent) (3-year average)']

# Filter for Prevalence of Undernourishment
undernourishment_data = data[data['Item'] == 'Prevalence of undernourishment (percent) (3-year average)']

# Extracting years
years = [col for col in data.columns if col.startswith('Y')]

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

# Plot Average Dietary Energy Supply Adequacy
for country in adequacy_data['Area'].unique():
    country_data = adequacy_data[adequacy_data['Area'] == country]
    axes[0].plot(years, country_data[years].values.flatten(), label=country)

axes[0].set_title('Average Dietary Energy Supply Adequacy Over the Years')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Adequacy (%)')
axes[0].legend()
axes[0].grid(True)

# Plot Prevalence of Undernourishment
for country in undernourishment_data['Area'].unique():
    country_data = undernourishment_data[undernourishment_data['Area'] == country]
    axes[1].plot(years, country_data[years].values.flatten(), label=country)

axes[1].set_title('Prevalence of Undernourishment Over the Years')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Undernourishment (%)')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()