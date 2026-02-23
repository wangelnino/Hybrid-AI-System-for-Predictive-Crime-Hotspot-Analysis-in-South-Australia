# Student Name: Tshering Sherpa
# Student FAN: sher0304
# File: ml_predictor.py
# Date: 19-11-2025
# Description: ML Predictor

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error
import joblib
import argparse
import warnings

warnings.filterwarnings('ignore')

class CrimePredictor:
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.historical_averages = {}
        
    def load_and_preprocess_data(self, data_path):
        """Load and preprocess with historical average feature"""
        print("Loading and preprocessing data...")
        df = pd.read_csv(data_path)
        df.columns = df.columns.str.strip()

        # Calculate historical averages for each suburb-crime combo
        self.historical_averages = df.groupby(['Suburb - Incident', 'Offence Level 2 Description'])['Total_Incidents'].mean().to_dict()
        
        # Add historical average as a feature
        df['historical_avg'] = df.apply(
            lambda row: self.historical_averages.get((row['Suburb - Incident'], row['Offence Level 2 Description']), df['Total_Incidents'].mean()), 
            axis=1
        )

        # Feature engineering
        categorical_cols = ['Suburb - Incident', 'Offence Level 2 Description']
        for col in categorical_cols:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col])
            self.label_encoders[col] = le

        # Enhanced feature set
        self.feature_columns = [
            'year', 'quarter', 'Suburb - Incident_encoded', 
            'Offence Level 2 Description_encoded', 'historical_avg'
        ]
        
        print(f"Training on {len(df)} samples")
        print(f"Features used: {self.feature_columns}")
        
        return df

    def train_models(self, data_path):
        """Train multiple ML models"""
        df = self.load_and_preprocess_data(data_path)
        
        X = df[self.feature_columns]
        y = df['Total_Incidents']

        tscv = TimeSeriesSplit(n_splits=3)
        model_performance = {}

        for model_name, model in self.models.items():
            print(f"Training {model_name}...")
            cv_scores = []
            
            for train_idx, val_idx in tscv.split(X):
                X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
                y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

                if model_name == 'linear_regression':
                    X_train_scaled = self.scaler.fit_transform(X_train)
                    X_val_scaled = self.scaler.transform(X_val)
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_val_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_val)

                mae = mean_absolute_error(y_val, y_pred)
                cv_scores.append(mae)

            avg_mae = np.mean(cv_scores)
            model_performance[model_name] = avg_mae
            print(f"{model_name} - Average MAE: {avg_mae:.4f}")

        # Select best model
        best_model_name = min(model_performance, key=model_performance.get)
        self.best_model = self.models[best_model_name]

        # Retrain best model on full dataset
        if best_model_name == 'linear_regression':
            X_scaled = self.scaler.fit_transform(X)
            self.best_model.fit(X_scaled, y)
        else:
            self.best_model.fit(X, y)

        print(f"\nBest model: {best_model_name} with MAE: {model_performance[best_model_name]:.4f}")

        # Save the trained model
        joblib.dump({
            'model': self.best_model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'model_name': best_model_name,
            'historical_averages': self.historical_averages
        }, 'trained_crime_model.joblib')

        return model_performance

    def predict(self, suburb, crime_type, quarter, year):
        """Make prediction with historical context"""
        try:
            model_data = joblib.load('trained_crime_model.joblib')
            self.best_model = model_data['model']
            self.label_encoders = model_data['label_encoders']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            historical_averages = model_data['historical_averages']

            # Encode categorical variables
            suburb_encoded = self.label_encoders['Suburb - Incident'].transform([suburb])[0]
            crime_encoded = self.label_encoders['Offence Level 2 Description'].transform([crime_type])[0]

            # Get historical average for this suburb-crime combo
            hist_avg = historical_averages.get((suburb, crime_type), 0)
            

            # Feature vector with historical average
            features = np.array([[year, quarter, suburb_encoded, crime_encoded, hist_avg]])

            if model_data['model_name'] == 'linear_regression':
                features_scaled = self.scaler.transform(features)
                prediction = self.best_model.predict(features_scaled)[0]
            else:
                prediction = self.best_model.predict(features)[0]

            # Ensure non-negative prediction
            prediction = max(0, round(prediction, 2))
            return prediction
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Enhanced Crime Prediction with Historical Averages')
    parser.add_argument('--train', action='store_true', help='Train models')
    parser.add_argument('--predict', action='store_true', help='Make prediction')
    parser.add_argument('--suburb', type=str, help='Suburb name')
    parser.add_argument('--crime_type', type=str, help='Crime type (Level 2)')
    parser.add_argument('--quarter', type=int, help='Quarter (1-4)')
    parser.add_argument('--year', type=int, help='Year')
    args = parser.parse_args()

    predictor = CrimePredictor()
    data_path = 'sa_crime_aggregated.csv'

    if args.train:
        performance = predictor.train_models(data_path)
        print("\nModel Performance Summary:")
        for model, mae in performance.items():
            print(f"{model}: MAE = {mae:.4f}")

    elif args.predict and args.suburb and args.crime_type and args.quarter and args.year:
        prediction = predictor.predict(args.suburb, args.crime_type, args.quarter, args.year)
        if prediction is not None:
            print(f"Predicted incidents for {args.suburb}, {args.crime_type} in Q{args.quarter} {args.year}: {prediction}")
        else:
            print("Prediction failed")
    else:
        print("Invalid arguments: See --help for usage.")

if __name__ == "__main__":
    main()