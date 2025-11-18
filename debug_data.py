import pandas as pd
import ast

# Load Data
print("Loading data...")
nj_precinct_data = pd.read_csv('precinct-data-congress-nj.csv', dtype={'GEOID20': str})
population_map = {str(row['GEOID20']): row['Total_2020_Total'] for _, row in nj_precinct_data.iterrows()}

nj_contiguity_df = pd.read_csv('Contiguity_nj.csv', header=None)
nj_contiguity_df.columns = ['Precinct', 'Neighbors']

print(f"Population map size: {len(population_map)}")
print(f"Contiguity map size: {len(nj_contiguity_df)}")

missing_neighbors = 0
total_neighbors = 0
precincts_with_all_missing_neighbors = []

for index, row in nj_contiguity_df.iterrows():
    precinct = str(row['Precinct'])
    neighbors = ast.literal_eval(row['Neighbors'])
    neighbors = [str(n) for n in neighbors]
    
    if not neighbors:
        continue
        
    missing_count = 0
    for n in neighbors:
        total_neighbors += 1
        if n not in population_map:
            missing_neighbors += 1
            missing_count += 1
            
    if missing_count == len(neighbors) and len(neighbors) > 0:
        precincts_with_all_missing_neighbors.append(precinct)

print(f"Total neighbors checked: {total_neighbors}")
print(f"Missing neighbors (not in population_map): {missing_neighbors}")
print(f"Precincts with ALL neighbors missing: {len(precincts_with_all_missing_neighbors)}")
if precincts_with_all_missing_neighbors:
    print(f"Example precincts with all missing neighbors: {precincts_with_all_missing_neighbors[:5]}")

# Check if any seed precincts (from the logic in main.ipynb) might be affected
# We can't easily replicate the seed logic without shapefiles, but we can check if the "stuck" behavior aligns.
