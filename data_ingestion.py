
# Student Name: Tshering Sherpa
# Student FAN: sher0304
# File: data_ingestion.py
# Date: 18-09-2025
# Description: Automated pipeline to fetch SA crime data via KaggleHub API and prepare it for time-series forecasting and hotspot analysis.


import pandas as pd
import kagglehub
from datetime import datetime

def main():
    # 1. AUTOMATED DATA FETCHING VIA KAGGLEHUB API
    print("Downloading crime data from Kaggle using kagglehub API...")
    try:
        dataset_path = kagglehub.dataset_download(
            "kanchana1990/south-australia-crime-data-2022-2023"
        )
        csv_path = f"{dataset_path}/2022-23_data_sa_crime.csv"
        df = pd.read_csv(csv_path)
        print("Dataset loaded successfully via KaggleHub API.")
        print(f"Initial data shape: {df.shape}")
    except Exception as e:
        print(f"Fatal error: Could not load dataset with KaggleHub. Error: {e}")
        return

    # 2. DATA CLEANING
    print("Cleaning data...")
    df_clean = df.copy()
    df_clean['Reported Date'] = pd.to_datetime(
        df_clean['Reported Date'], format='%d/%m/%Y', errors='coerce'
    )
    critical_columns = ['Reported Date', 'Suburb - Incident', 'Offence Level 2 Description']
    df_clean.dropna(subset=critical_columns, inplace=True)
    df_clean['Offence count'] = pd.to_numeric(df_clean['Offence count'], errors='coerce')
    df_clean['Offence count'].fillna(1, inplace=True)
    print(f"Data shape after cleaning: {df_clean.shape}")

    # 3. FEATURE ENGINEERING: YEAR and QUARTER
    df_clean['year'] = df_clean['Reported Date'].dt.year
    df_clean['quarter'] = df_clean['Reported Date'].dt.quarter
    print("\n=== CRIME CATEGORY ANALYSIS ===")
    print(df_clean['Offence Level 2 Description'].value_counts())

    # 4. AGGREGATE BY SUBURB, OFFENCE, YEAR, QUARTER
    print("Aggregating data by Suburb, Crime Type (Level 2), Year, and Quarter...")
    aggregated_df = df_clean.groupby(
        ['Suburb - Incident', 'Offence Level 2 Description', 'year', 'quarter']
    ).agg(Total_Incidents=('Offence count', 'sum')).reset_index()

    # 5. QUALITY FILTER: Only keep combos with >=2 quarters of data (change threshold as needed)
    ts_readiness = aggregated_df.groupby(
        ['Suburb - Incident', 'Offence Level 2 Description']
    ).size().reset_index(name='quarter_count')
    valid_series = ts_readiness[ts_readiness['quarter_count'] >= 2]
    filtered_df = aggregated_df.merge(
        valid_series,
        on=['Suburb - Incident', 'Offence Level 2 Description'],
        how='inner'
    )

    print(f"\nAggregated data shape: {aggregated_df.shape}")
    print(f"Filtered data shape (only series with >=2 quarters): {filtered_df.shape}")
    print(f"Number of unique suburb-crime combinations: {len(valid_series)}")
    print("\nFinal crime types (Level 2) after filtering:")
    print(filtered_df['Offence Level 2 Description'].value_counts())

    # 6. SAVE CLEANED DATA
    output_filename = 'sa_crime_aggregated.csv'
    filtered_df.to_csv(output_filename, index=False)
    print(f"\nPipeline complete! Quarterly aggregated data saved to {output_filename}.")

    # 7. SAMPLE OUTPUT
    print("\nSample of the final aggregated dataset (Quarterly):")
    print(filtered_df.head(20))

if __name__ == "__main__":
    main()
