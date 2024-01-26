import pandas as pd

# Load the population dataset
file_path = r"..\..\data\raw\Population_E_Asia\Population_E_Asia_NOFLAG.csv"

try:
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
except Exception as e:
    print("Error reading the population file:", e)
else:
    # List of South Asian countries to include
    south_asian_countries = ['India', 'Pakistan', 'Bangladesh', 'Nepal', 'Bhutan']

    # Filter the data to include only the selected South Asian countries
    filtered_data = data[data['Area'].isin(south_asian_countries)]

    # Save the filtered data to a new CSV file
    output_file_path = r"..\..\data\processed\Population_Data\Population_S_Asia_NOFLAG.csv"
    filtered_data.to_csv(output_file_path, index=False)
