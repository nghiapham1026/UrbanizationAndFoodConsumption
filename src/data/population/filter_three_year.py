import pandas as pd

# Load the population data
# Replace 'population_data.csv' with the path to your CSV file
population_data = pd.read_csv(r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv", encoding='ISO-8859-1')

# List of all year columns
year_columns = [col for col in population_data.columns if col.startswith('Y') and len(col) == 5]

# New DataFrame to store the average values
population_data_avg = population_data[['Area Code', 'Area Code (M49)', 'Area', 'Item Code', 'Item', 'Element Code', 'Element', 'Unit']].copy()

# Calculate the average value for three-year periods and store in new columns
for i in range(0, len(year_columns), 3):
    # Check if there are at least 3 years left, if not, break the loop
    if i + 2 < len(year_columns):
        years = year_columns[i:i+3]
        avg_col_name = f'Y{years[0][1:]}{years[-1][1:]}'
        population_data_avg[avg_col_name] = population_data[years].mean(axis=1)

# Save the new dataset to a CSV file
# Replace 'averaged_population_data.csv' with the desired path for your new CSV file
population_data_avg.to_csv(r"..\..\..\data\processed\Population_Data\Total_Urban_Populations_3_year.csv", index=False)
