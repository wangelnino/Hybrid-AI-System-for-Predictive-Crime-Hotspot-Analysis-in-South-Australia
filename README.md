Special Instructions to Run the Code
i. Kaggle Account & Authentication Mandatory:

You must have a Kaggle account. The script uses the kagglehub API to fetch data.

On first run, the library will handle authentication. If you are not already logged in on your system, it will prompt you to authenticate via your browser. This is a required step.

ii. Install from requirements.txt:

The code requires specific packages. Install them exactly using:

bash
pip install -r requirements.txt

iii. Follow these steps before providing input to the system (in bash):

a.Ingest and clean new crime data (python data_ingestion.py).

b.Generate updated symbolic knowledge base (python generate_average.py).

c. If training, run and validate model (python ml_predictor.py --train).
