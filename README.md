# Crime Rate Prediction

A Flask-based machine learning web application that predicts crime rates for major Indian metropolitan cities. The app uses historical NCRB-style crime data, a trained Random Forest regression model, and an interactive dashboard to show forecasts, trends, rankings, estimated cases, risk categories, and safety helplines.

## Overview

This project forecasts crime rates for 19 Indian cities across 10 crime categories. Users can select a city, crime type, and forecast year, then view a detailed analytics dashboard with:

- Predicted crime rate and estimated case count
- Risk category classification
- Historical trend plus forecast point
- City-wise comparison and ranking
- Safest and highest-risk city lists
- Model evaluation metrics
- Category-specific emergency and support helplines
- CSV export for the selected prediction

The training data covers 2014 to 2021, and the web app supports forecast years from 2022 to 2030.

## Supported Cities

Ahmedabad, Bengaluru, Chennai, Coimbatore, Delhi, Ghaziabad, Hyderabad, Indore, Jaipur, Kanpur, Kochi, Kolkata, Kozhikode, Lucknow, Mumbai, Nagpur, Patna, Pune, and Surat.

## Supported Crime Categories

- Crime Committed by Juveniles
- Crime against SC
- Crime against ST
- Crime against Senior Citizen
- Crime against children
- Crime against women
- Cyber Crimes
- Economic Offences
- Kidnapping
- Murder

## Tech Stack

- Python
- Flask
- Pandas
- NumPy
- scikit-learn
- OpenPyXL
- HTML, CSS, and JavaScript
- Pickle for saved model loading

## Project Structure

```text
Crime-Rate-Prediction-main/
|-- app.py                         # Flask application and prediction logic
|-- crp.ipynb                      # Notebook used for model/data work
|-- requirements.txt               # Python dependencies
|-- Dataset/
|   |-- crp.xlsx
|   |-- new_dataset.xlsx
|   `-- new_dataset_copy.xlsx
|-- Mappings/
|   |-- City_Mapping.txt
|   `-- Type_Mapping.txt
|-- Model/
|   `-- model.pkl                  # Trained Random Forest model
|-- Report/
|   |-- Ansh_Gupta_MiniProject.docx
|   |-- Ansh_Gupta_Mini_Project_Presentation.pptx
|   `-- literature survey.xlsx
|-- static/
|   |-- main.js
|   |-- styles.css
|   `-- images/
`-- templates/
    |-- index.html
    `-- result.html
```

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd Crime-Rate-Prediction-main
```

2. Create and activate a virtual environment:

```bash
python -m venv myenv
```

On Windows:

```bash
myenv\Scripts\activate
```

On macOS/Linux:

```bash
source myenv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Usage

1. Choose a city.
2. Choose a crime category.
3. Choose a forecast year between 2022 and 2030.
4. Click `Predict Crime Rate`.
5. Review the analytics dashboard.
6. Use `Download CSV` to export the selected prediction.

## API Endpoint

The app also exposes a JSON prediction endpoint:

```text
GET /api/predict?city=<city_code>&crime=<crime_code>&year=<year>
```

Example:

```text
http://127.0.0.1:5000/api/predict?city=4&crime=9&year=2025
```

This returns the prediction payload for Delhi, Murder, and year 2025.

## Other Routes

```text
/                       Home page
/predict                Form submission route
/api/predict            JSON prediction API
/download-prediction    CSV download route
/report                 Opens the detailed project report
```

## Model Details

The saved model is loaded from `Model/model.pkl`. It predicts crime rate using:

- Year
- City code
- Estimated population
- Crime type code

The app estimates population from the stored 2011 population values and uses the prediction result to calculate estimated cases and risk category.

## Dataset

The dataset is stored in the `Dataset/` folder and contains historical crime records for supported cities and crime categories. The main runtime dataset used by the Flask app is:

```text
Dataset/new_dataset.xlsx
```

## Notes

- Keep `Model/model.pkl` and `Dataset/new_dataset.xlsx` in their current paths because `app.py` loads them directly.
- The project report can be opened from the app through the `View Detailed Project Report` link.
- Forecasts are intended for educational and analytical use, not as a substitute for official crime statistics or emergency decision-making.

## Author

Developed by Ansh Gupta.

- LinkedIn: <https://www.linkedin.com/in/ansh-gupta-iiitr>
- GitHub: <https://github.com/ansh-34>
