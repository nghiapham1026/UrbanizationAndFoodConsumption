import pandas as pd

# Load the food security dataset
new_file_path = r"..\..\data\raw\Food_Security_Data_E_Asia\Food_Security_Data_E_Asia_NOFLAG.csv"

try:
    new_data = pd.read_csv(new_file_path, encoding='ISO-8859-1')
except Exception as e:
    print("Error reading the food security file:", e)
else:
    # List of South Asian countries to include
    south_asian_countries = ['India', 'Pakistan', 'Bangladesh', 'Nepal', 'Bhutan']

    # Filter the data to include only the selected South Asian countries
    filtered_new_data = new_data[new_data['Area'].isin(south_asian_countries)]

    # Save the filtered data to a new CSV file
    output_new_file_path = r"..\..\data\processed\Food_Security_Data\Food_Security_Data_S_Asia_NOFLAG.csv"
    filtered_new_data.to_csv(output_new_file_path, index=False)
