from typing import Final, final
import pandas as pd

@final
def extract_relevant_data(df, element, item) -> pd.DataFrame:
    interval_columns: Final = [col for col in df.columns if 'Y' in col and len(col) == 9]
    return df[df['Element'] == element][['Area'] + interval_columns] if element else df[df['Item'] == item][['Area'] + interval_columns]

def reset_data(population_data_avg, population_data_processed):
    global urban_population, total_population, urban_data, total_pop_data

    urban_population = extract_relevant_data(population_data_avg, 'Urban population', None)
    total_population = extract_relevant_data(population_data_avg, 'Total Population - Both sexes', None)
    urban_data = population_data_processed[population_data_processed['Element'] == 'Urban population']
    total_pop_data = population_data_processed[population_data_processed['Element'] == 'Total Population - Both sexes']
    urban_population_melted = urban_population.melt(id_vars='Area', var_name='Year', value_name='Urban Population')
    total_population_melted = total_population.melt(id_vars='Area', var_name='Year', value_name='Total Population')
