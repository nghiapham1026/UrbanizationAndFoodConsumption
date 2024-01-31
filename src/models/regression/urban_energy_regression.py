import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import statsmodels.api as sm

# Load datasets
dietary_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"
urban_pop_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv"

dietary_data = pd.read_csv(dietary_path, encoding='ISO-8859-1')
urban_data = pd.read_csv(urban_pop_path, encoding='ISO-8859-1')
total_pop_data = urban_data[urban_data['Element'] == 'Total Population - Both sexes']

# Filter for 'Average dietary energy requirement' and 'Urban population'
dietary_data = dietary_data[dietary_data['Item'] == 'Average dietary energy requirement (kcal/cap/day)']
urban_data = urban_data[urban_data['Element'] == 'Urban population']

# Convert year columns to numeric and set index to 'Area' for both datasets
year_columns = [col for col in dietary_data.columns if col.startswith('Y') and len(col) == 5]
dietary_data[year_columns] = dietary_data[year_columns].apply(pd.to_numeric, errors='coerce')
dietary_data.set_index('Area', inplace=True)
total_pop_data.set_index('Area', inplace=True)
urban_data.set_index('Area', inplace=True)

merged_data_list = []

# Ensure only matching years and countries are merged
common_years = set(year_columns).intersection(urban_data.columns).intersection(total_pop_data.columns)
common_countries = list(set(dietary_data.index).intersection(urban_data.index).intersection(total_pop_data.index))

for year in common_years:
    urban_percentage = (urban_data.loc[common_countries, year] / total_pop_data.loc[common_countries, year]) * 100
    temp_df = pd.DataFrame({
        'Area': common_countries,
        'Year': int(year[1:]),
        'AverageDietaryEnergy': dietary_data.loc[common_countries, year].values,
        'UrbanPopulationPercentage': urban_percentage.values
    })
    merged_data_list.append(temp_df)

# Concatenate all dataframes in the list
merged_data = pd.concat(merged_data_list, ignore_index=True)

# Drop rows with NaN values and duplicates
merged_data.dropna(inplace=True)
merged_data.drop_duplicates(inplace=True)

plt.figure(figsize=(15, 10))

# Loop through each country and perform regression
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]
    X = country_data['UrbanPopulationPercentage']
    y = country_data['AverageDietaryEnergy']
    X = sm.add_constant(X)  # Adds a constant term to the predictor
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)

    # Plotting each country's data and regression line
    plt.scatter(country_data['UrbanPopulationPercentage'], country_data['AverageDietaryEnergy'], label=f'{country} Data')
    plt.plot(country_data['UrbanPopulationPercentage'], predictions, label=f'{country} Regression')

plt.title('Urban Population Percentage vs Average Dietary Energy Requirement by Country')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Average Dietary Energy (kcal/cap/day)')
plt.legend()
plt.grid(True)
plt.show()