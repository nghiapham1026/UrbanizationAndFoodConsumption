import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv(r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv", encoding='ISO-8859-1')

# Filter for 'Number of people undernourished'
undernourished_data = data[data['Item'] == 'Number of people undernourished (million) (3-year average)']

# Select only columns with three-year average data
three_year_avg_columns = [col for col in undernourished_data.columns if 'Y' in col and len(col) == 9]

# Plot
plt.figure(figsize=(10, 6))
for country in undernourished_data['Area'].unique():
    country_data = undernourished_data[undernourished_data['Area'] == country]
    plt.plot(three_year_avg_columns, country_data[three_year_avg_columns].values.flatten(), label=country)

plt.title('Number of People Undernourished Over the Years (3-Year Average)')
plt.xlabel('Year')
plt.ylabel('Number of People (Millions)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjust layout
plt.show()
