import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the datasets
population_data_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations_3_year.csv"
dietary_data_path = r"..\..\..\data\processed\Food_Security_Data\Food_Security_S_Asia_NOFLAG.csv"

population_data = pd.read_csv(population_data_path, encoding='ISO-8859-1')
dietary_data = pd.read_csv(dietary_data_path, encoding='ISO-8859-1')

# Extract relevant columns including 'Area'
def extract_relevant_data(df, element, item):
    interval_columns = [col for col in df.columns if 'Y' in col and len(col) == 9]
    return df[df['Element'] == element][['Area'] + interval_columns] if element else df[df['Item'] == item][['Area'] + interval_columns]

# Extract data for urban population, total population, and fat intake
urban_population = extract_relevant_data(population_data, 'Urban population', None)
total_population = extract_relevant_data(population_data, 'Total Population - Both sexes', None)
fat_intake = extract_relevant_data(dietary_data, None, 'Average fat supply (g/cap/day) (3-year average)')

# Reshape the data for merging
urban_population_melted = urban_population.melt(id_vars='Area', var_name='Year', value_name='Urban Population')
total_population_melted = total_population.melt(id_vars='Area', var_name='Year', value_name='Total Population')
fat_intake_melted = fat_intake.melt(id_vars='Area', var_name='Year', value_name='Fat Intake')
# Merge the datasets
merged_data = pd.merge(pd.merge(urban_population_melted, total_population_melted, on=['Area', 'Year']), fat_intake_melted, on=['Area', 'Year'])

# Calculate Urban Population Percentage
merged_data['Urban Population Percentage'] = (merged_data['Urban Population'] / merged_data['Total Population']) * 100

# Drop NaN values
merged_data.dropna(subset=['Urban Population Percentage', 'Fat Intake'], inplace=True)

plt.figure(figsize=(15, 10))

# Loop through each country and perform regression
for country in merged_data['Area'].unique():
    country_data = merged_data[merged_data['Area'] == country]
    X = country_data['Urban Population Percentage']
    y = country_data['Fat Intake']
    X = sm.add_constant(X)  # Adds a constant term to the predictor
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)

    # Plotting each country's data and regression line
    plt.scatter(country_data['Urban Population Percentage'], country_data['Fat Intake'], label=f'{country} Data')
    plt.plot(country_data['Urban Population Percentage'], predictions, label=f'{country} Regression')

plt.title('Urban Population Percentage vs Fat Intake by Country')
plt.xlabel('Urban Population Percentage')
plt.ylabel('Fat Intake (kcal/cap/day)')
plt.legend()
plt.grid(True)
plt.show()
