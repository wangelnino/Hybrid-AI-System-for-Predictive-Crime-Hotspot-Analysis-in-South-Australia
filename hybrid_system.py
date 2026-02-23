# File: hybrid_system.py
# Date: 19-11-2025
# Description: Main hybrid system integrating ML prediction and symbolic reasoning

import subprocess
import argparse
import os

class HybridCrimeSystem:
    def __init__(self):
        pass
        
    def query_prolog(self, suburb, crime_type, year, quarter, predicted_count):
        """Query Prolog engine for classification and reasoning (quarterly version)"""
        try:
            cmd = [
                'swipl', '-q', '-s', 'symbolic_reasoner.pl', 
                '-g', (
                    f"reason_about_prediction('{suburb}', '{crime_type}', {year}, {quarter}, {predicted_count}, C, J), "
                    "write(C), nl, write(J), nl, halt."
                )
            ]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = output.split('\n')
                if len(lines) >= 2:
                    classification = lines[0].strip()
                    justification = lines[1].strip()
                    return classification, justification
                else:
                    return "Parse Error", f"Unexpected output format: {output}"
            else:
                return "Execution Error", f"Prolog failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Timeout", "Prolog query timed out"
        except Exception as e:
            return "Error", f"Prolog communication error: {str(e)}"
    
    def run_demo(self):
        """Run comprehensive demonstration of the hybrid system"""
        print("=" * 60)
        print("HYBRID AI SYSTEM DEMONSTRATION")
        print("Crime Prediction and Hotspot Analysis System (Quarterly)")
        print("=" * 60)
        
        # Example test cases
        test_cases = [
        # CRITICAL HOTSPOT: Very high absolute count
        {'suburb': 'ADELAIDE', 'crime_type': 'THEFT AND RELATED OFFENCES', 'year': 2025, 'quarter': 3, 'prediction': 1200},
        
        # SIGNIFICANT HOTSPOT: 3x historical average + >10 incidents
        {'suburb': 'ABERFOYLE PARK', 'crime_type': 'THEFT AND RELATED OFFENCES', 'year': 2025, 'quarter': 3, 'prediction': 60},
        
        # EMERGING HOTSPOT: 2x historical average + >5 incidents  
        {'suburb': 'ALBERTON', 'crime_type': 'THEFT AND RELATED OFFENCES', 'year': 2025, 'quarter': 3, 'prediction': 70},
        
        # STABLE: Within normal range
        {'suburb': 'ABERFOYLE PARK', 'crime_type': 'ACTS INTENDED TO CAUSE INJURY', 'year': 2025, 'quarter': 3, 'prediction': 20},
        
        # LOW RISK: Below 5 incidents
        {'suburb': 'ALDGATE', 'crime_type': 'THEFT AND RELATED OFFENCES', 'year': 2025, 'quarter': 3, 'prediction': 3}
    ]
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*50}")
            print(f"TEST CASE {i}")
            print(f"{'='*50}")
            # ML Prediction (simulated)
            print("STEP 1: Machine Learning Prediction")
            print(f"Input: {test_case}")
            predicted_count = test_case['prediction']
            print(f"Predicted Incident Count: {predicted_count}")
            # Symbolic Reasoning
            print("\nSTEP 2: Symbolic Reasoning")
            classification, justification = self.query_prolog(
                test_case['suburb'], 
                test_case['crime_type'], 
                test_case['year'],
                test_case['quarter'],
                predicted_count
            )
            print(f"Hotspot Classification: {classification}")
            print(f"Justification: {justification}")
            # Recommendation
            print("\nSTEP 3: Actionable Recommendation")
            self.generate_recommendation(classification, predicted_count, test_case['suburb'], test_case['crime_type'])
            results.append({
                **test_case,
                'classification': classification,
                'justification': justification
            })
        
        # Summary
        print(f"\n{'='*60}")
        print("DEMONSTRATION SUMMARY")
        print(f"{'='*60}")
        for result in results:
            print(f"\nSuburb: {result['suburb']}")
            print(f"Crime Type: {result['crime_type']}")
            print(f"Year: {result['year']} Quarter: {result['quarter']}")
            print(f"Predicted: {result['prediction']} incidents")
            print(f"Classification: {result['classification']}")
            print(f"Justification: {result['justification']}")
    
    def run_single_prediction(self, suburb, crime_type, year, quarter, prediction_value):
        """Run prediction and reasoning for single input"""
        print(f"\nRunning Hybrid AI Analysis for:")
        print(f"Suburb: {suburb}")
        print(f"Crime Type: {crime_type}")
        print(f"Year: {year}, Quarter: {quarter}")
        print("\n1. MACHINE LEARNING PREDICTION:")
        print(f"Predicted Incident Count: {prediction_value}")
        print("\n2. SYMBOLIC REASONING:")
        classification, justification = self.query_prolog(suburb, crime_type, year, quarter, prediction_value)
        print(f"Hotspot Classification: {classification}")
        print(f"Justification: {justification}")
        print("\n3. ACTIONABLE RECOMMENDATION:")
        self.generate_recommendation(classification, prediction_value, suburb, crime_type)
    
    def generate_recommendation(self, classification, count, suburb, crime_type):
        """Generate actionable recommendations based on classification"""
        recommendations = {
            'Critical Hotspot': f"🚨 IMMEDIATE ACTION REQUIRED: Deploy additional patrols to {suburb} for {crime_type}. Consider tactical response team deployment.",
            'Significant Hotspot': f"🔴 HIGH PRIORITY: Increase police presence in {suburb}. Review recent incidents and implement targeted prevention strategies.",
            'Emerging Hotspot': f"🟡 MONITOR CLOSELY: Enhanced monitoring recommended for {suburb}. Consider community engagement initiatives.",
            'Stable': f"🟢 MAINTAIN CURRENT: {suburb} shows stable patterns for {crime_type}. Continue standard patrol routes.",
            'Low Risk': f"🔵 MINIMAL CONCERN: {suburb} has low predicted {crime_type} incidents. Focus resources on higher-risk areas."
        }
        recommendation = recommendations.get(classification, 
            f"⚪ REVIEW REQUIRED: Manual assessment recommended for {suburb}.")
        print(recommendation)

def main():
    parser = argparse.ArgumentParser(description='Hybrid AI Crime Prediction System (Quarterly)')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--predict', action='store_true', help='Run single prediction')
    parser.add_argument('--suburb', type=str, help='Suburb name')
    parser.add_argument('--crime_type', type=str, help='Crime type (Level 2)')
    parser.add_argument('--year', type=int, help='Year')
    parser.add_argument('--quarter', type=int, help='Quarter (1-4)')
    parser.add_argument('--prediction', type=float, help='Predicted incident count')
    args = parser.parse_args()
    system = HybridCrimeSystem()
    if args.demo:
        system.run_demo()
    elif args.predict and args.suburb and args.crime_type and args.year and args.quarter and args.prediction is not None:
        system.run_single_prediction(args.suburb, args.crime_type, args.year, args.quarter, args.prediction)
    else:
        print("Usage:")
        print("  Demo: python hybrid_system.py --demo")
        print("  Single prediction: python hybrid_system.py --predict --suburb 'ADELAIDE' --crime_type 'THEFT AND RELATED OFFENCES' --year 2025 --quarter 3 --prediction 48.5")

if __name__ == "__main__":
    main()
