# Student Name: Tshering Sherpa
# Student FAN: sher0304
# File: generate_average.py
# Date: 15-11-2025
# Description: Generating crime_averages prolog file for symbolic_reasoner prolog

import pandas as pd

filename = 'sa_crime_aggregated.csv'  
data = pd.read_csv(filename)

# Fix stray whitespace if needed
data.columns = data.columns.str.strip()
print(f"Columns in dataset: {list(data.columns)}")  

# Group by suburb, offence type, year, and quarter for averages
grouped = data.groupby(['Suburb - Incident', 'Offence Level 2 Description', 'year', 'quarter']).agg({'Total_Incidents': 'mean'}).reset_index()

# Export as Prolog facts: historical_average('SUBURB', 'CRIME_TYPE', YEAR, QUARTER, AVG).
with open('crime_averages.pl', 'w') as f:
    for row in grouped.itertuples(index=False):
        suburb_fixed = str(row[0]).replace("'", "''")
        crime_type_fixed = str(row[1]).replace("'", "''")
        year = int(row[2])
        quarter = int(row[3])
        avg = round(row[4], 2)
        f.write(f"historical_average('{suburb_fixed}', '{crime_type_fixed}', {year}, {quarter}, {avg}).\n")

print(f"crime_averages.pl file created with quarterly averages.")


