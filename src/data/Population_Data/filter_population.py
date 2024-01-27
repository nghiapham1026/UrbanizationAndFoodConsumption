import pandas as pd

# Load dataset
file_path = r"..\..\..\data\processed\Population_Data\Population_S_Asia_NOFLAG.csv"  # Replace with your actual file path
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Define the items to keep
items_to_keep = ['Total Population - Both sexes', 'Urban population']

# Filter the dataset
filtered_data = data[data['Element'].isin(items_to_keep)]

# Save the filtered dataset to a new CSV file
output_file_path = r"..\..\..\data\processed\Population_Data\Total_Urban_Populations.csv"  # Replace with your desired output file path
filtered_data.to_csv(output_file_path, index=False)