from flask import Flask, Response, jsonify, render_template, request, send_from_directory
import csv
import io
import math
import pickle

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


model = pickle.load(open("Model/model.pkl", "rb"))
dataset = pd.read_excel("Dataset/new_dataset.xlsx")

app = Flask(__name__)

REPORT_DIR = "Report"
REPORT_FILE = "Ansh_Gupta_MiniProject.docx"

CITY_NAMES = {
    "0": "Ahmedabad",
    "1": "Bengaluru",
    "2": "Chennai",
    "3": "Coimbatore",
    "4": "Delhi",
    "5": "Ghaziabad",
    "6": "Hyderabad",
    "7": "Indore",
    "8": "Jaipur",
    "9": "Kanpur",
    "10": "Kochi",
    "11": "Kolkata",
    "12": "Kozhikode",
    "13": "Lucknow",
    "14": "Mumbai",
    "15": "Nagpur",
    "16": "Patna",
    "17": "Pune",
    "18": "Surat",
}

CRIME_NAMES = {
    "0": "Crime Committed by Juveniles",
    "1": "Crime against SC",
    "2": "Crime against ST",
    "3": "Crime against Senior Citizen",
    "4": "Crime against children",
    "5": "Crime against women",
    "6": "Cyber Crimes",
    "7": "Economic Offences",
    "8": "Kidnapping",
    "9": "Murder",
}

POPULATION = {
    "0": 63.50,
    "1": 85.00,
    "2": 87.00,
    "3": 21.50,
    "4": 163.10,
    "5": 23.60,
    "6": 77.50,
    "7": 21.70,
    "8": 30.70,
    "9": 29.20,
    "10": 21.20,
    "11": 141.10,
    "12": 20.30,
    "13": 29.00,
    "14": 184.10,
    "15": 25.00,
    "16": 20.50,
    "17": 50.50,
    "18": 45.80,
}

CITY_CODES = {name: code for code, name in CITY_NAMES.items()}
CRIME_CODES = {name: code for code, name in CRIME_NAMES.items()}
FORECAST_YEARS = range(2022, 2031)

HELPLINES = {
    "default": {
        "title": "Emergency / Police Support",
        "summary": "Use these contacts if there is immediate danger, violence, or an active crime situation.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Police, fire, and ambulance emergency support"},
            {"label": "Police", "number": "100", "note": "Traditional police helpline, where available"},
        ],
    },
    "0": {
        "title": "Juvenile / Child Safety Support",
        "summary": "For incidents involving minors, child distress, exploitation, or unsafe situations.",
        "contacts": [
            {"label": "Child Helpline", "number": "1098", "note": "Children in distress"},
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate danger or police help"},
        ],
    },
    "1": {
        "title": "SC Safety / Police Support",
        "summary": "For caste-based violence, threats, harassment, or immediate safety concerns.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate police help"},
            {"label": "Police", "number": "100", "note": "Report crime at the nearest police station"},
        ],
    },
    "2": {
        "title": "ST Safety / Police Support",
        "summary": "For caste/tribe-based violence, threats, harassment, or immediate safety concerns.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate police help"},
            {"label": "Police", "number": "100", "note": "Report crime at the nearest police station"},
        ],
    },
    "3": {
        "title": "Senior Citizen Support",
        "summary": "For elder abuse, neglect, distress, safety concerns, or guidance for senior citizens.",
        "contacts": [
            {"label": "Elderline", "number": "14567", "note": "National helpline for senior citizens"},
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate danger or police help"},
        ],
    },
    "4": {
        "title": "Child Safety Support",
        "summary": "For crimes against children, exploitation, abuse, trafficking, or a child in distress.",
        "contacts": [
            {"label": "Child Helpline", "number": "1098", "note": "Children in distress"},
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate danger or police help"},
        ],
    },
    "5": {
        "title": "Women Safety Support",
        "summary": "For violence, harassment, stalking, domestic abuse, or immediate safety support.",
        "contacts": [
            {"label": "Women Helpline", "number": "181", "note": "Women in distress"},
            {"label": "Women Police Helpline", "number": "1091", "note": "Police support for women"},
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate danger"},
        ],
    },
    "6": {
        "title": "Cybercrime Support",
        "summary": "For online fraud, phishing, cyberstalking, account hacking, or digital extortion.",
        "contacts": [
            {"label": "Cyber Crime Helpline", "number": "1930", "note": "Report financial cyber fraud quickly"},
            {"label": "Cybercrime Portal", "number": "cybercrime.gov.in", "note": "File an online cybercrime complaint"},
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate physical danger"},
        ],
    },
    "7": {
        "title": "Economic Offence Support",
        "summary": "For fraud, cheating, financial crime, or online banking/payment fraud.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Police support for active crime"},
            {"label": "Cyber Crime Helpline", "number": "1930", "note": "Use for online or banking cyber fraud"},
            {"label": "Police", "number": "100", "note": "Report financial offences locally"},
        ],
    },
    "8": {
        "title": "Kidnapping / Missing Person Support",
        "summary": "For kidnapping, abduction, missing child/person, or suspected trafficking.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Immediate police help"},
            {"label": "Child Helpline", "number": "1098", "note": "If a child is involved"},
            {"label": "Police", "number": "100", "note": "Report to police without delay"},
        ],
    },
    "9": {
        "title": "Violent Crime Support",
        "summary": "For murder, assault, life-threatening violence, or urgent police/medical response.",
        "contacts": [
            {"label": "Emergency Response Support System", "number": "112", "note": "Police, fire, and ambulance support"},
            {"label": "Police", "number": "100", "note": "Traditional police helpline, where available"},
            {"label": "Ambulance", "number": "108", "note": "Medical emergency response"},
        ],
    },
}


def estimate_population(city_code, year):
    base_population = POPULATION[city_code]
    year_diff = int(year) - 2011
    return base_population + 0.01 * year_diff * base_population


def predict_crime_rate(city_code, crime_code, year):
    population = estimate_population(city_code, year)
    rate = float(model.predict([[int(year), int(city_code), population, int(crime_code)]])[0])
    return max(rate, 0), population


def classify_risk(crime_rate):
    if crime_rate <= 1:
        return "Very Low Crime Area"
    if crime_rate <= 5:
        return "Low Crime Area"
    if crime_rate <= 15:
        return "High Crime Area"
    return "Very High Crime Area"


def build_city_comparison(crime_code, year):
    comparison = []
    for city_code, city_name in CITY_NAMES.items():
        rate, population = predict_crime_rate(city_code, crime_code, year)
        comparison.append(
            {
                "city": city_name,
                "city_code": city_code,
                "rate": round(rate, 2),
                "cases": math.ceil(rate * population),
                "status": classify_risk(rate),
            }
        )
    return sorted(comparison, key=lambda item: item["rate"], reverse=True)


def build_history(city_name, crime_type, predicted_rate, year):
    rows = dataset[(dataset["City"] == city_name) & (dataset["Type"] == crime_type)]
    rows = rows.sort_values("Year")
    history = [
        {"year": int(row["Year"]), "rate": round(float(row["Crime Rate"]), 2), "kind": "Actual"}
        for _, row in rows.iterrows()
    ]
    history.append({"year": int(year), "rate": round(predicted_rate, 2), "kind": "Forecast"})
    return history


def build_actual_vs_predicted(city_name, crime_type):
    rows = dataset[(dataset["City"] == city_name) & (dataset["Type"] == crime_type)]
    rows = rows.sort_values("Year")
    points = []
    city_code = CITY_CODES[city_name]
    crime_code = CRIME_CODES[crime_type]
    for _, row in rows.iterrows():
        year = int(row["Year"])
        predicted, _ = predict_crime_rate(city_code, crime_code, year)
        points.append(
            {
                "year": year,
                "actual": round(float(row["Crime Rate"]), 2),
                "predicted": round(predicted, 2),
            }
        )
    return points


def build_city_crime_table(city_code, year):
    rows = []
    for crime_code, crime_type in CRIME_NAMES.items():
        rate, population = predict_crime_rate(city_code, crime_code, year)
        rows.append(
            {
                "crime": crime_type,
                "rate": round(rate, 2),
                "cases": math.ceil(rate * population),
                "status": classify_risk(rate),
            }
        )
    return sorted(rows, key=lambda item: item["rate"], reverse=True)


def build_model_metrics():
    encoded = dataset.copy()
    encoded["city_code"] = encoded["City"].map(CITY_CODES).astype(int)
    encoded["crime_code"] = encoded["Type"].map(CRIME_CODES).astype(int)
    x_values = encoded[["Year", "city_code", "Population (in Lakhs) (2011)+", "crime_code"]].to_numpy()
    y_true = encoded["Crime Rate"]
    y_pred = model.predict(x_values)
    return {
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(mean_squared_error(y_true, y_pred, squared=False)), 2),
        "records": int(len(encoded)),
    }


def build_prediction_payload(city_code, crime_code, year):
    city_name = CITY_NAMES[city_code]
    crime_type = CRIME_NAMES[crime_code]
    crime_rate, population = predict_crime_rate(city_code, crime_code, year)
    cases = math.ceil(crime_rate * population)
    city_average = float(
        dataset[(dataset["City"] == city_name) & (dataset["Type"] == crime_type)]["Crime Rate"].mean()
    )
    comparison = build_city_comparison(crime_code, year)
    selected_rank = next(
        index + 1 for index, item in enumerate(comparison) if item["city_code"] == city_code
    )
    actual_rows = dataset[(dataset["City"] == city_name) & (dataset["Type"] == crime_type)].sort_values("Year")
    first_rate = float(actual_rows.iloc[0]["Crime Rate"])
    last_rate = float(actual_rows.iloc[-1]["Crime Rate"])
    trend_delta = last_rate - first_rate
    trend_label = "Increasing" if trend_delta > 0 else "Decreasing" if trend_delta < 0 else "Stable"

    return {
        "city_code": city_code,
        "crime_code": crime_code,
        "city_name": city_name,
        "crime_type": crime_type,
        "year": int(year),
        "crime_status": classify_risk(crime_rate),
        "crime_rate": round(crime_rate, 2),
        "cases": cases,
        "population": round(population, 2),
        "city_average": round(city_average, 2),
        "average_delta": round(crime_rate - city_average, 2),
        "selected_rank": selected_rank,
        "total_cities": len(comparison),
        "trend_label": trend_label,
        "trend_delta": round(trend_delta, 2),
        "history": build_history(city_name, crime_type, crime_rate, year),
        "comparison": comparison,
        "safest_cities": sorted(comparison, key=lambda item: item["rate"])[:5],
        "riskiest_cities": comparison[:5],
        "crime_table": build_city_crime_table(city_code, year),
        "actual_vs_predicted": build_actual_vs_predicted(city_name, crime_type),
        "model_metrics": build_model_metrics(),
        "helpline": HELPLINES.get(crime_code, HELPLINES["default"]),
    }


@app.route("/")
def index():
    return render_template("index.html", forecast_years=FORECAST_YEARS)


@app.route("/predict", methods=["POST"])
def predict_result():
    payload = build_prediction_payload(
        request.form["city"],
        request.form["crime"],
        request.form["year"],
    )
    return render_template("result.html", **payload)


@app.route("/api/predict")
def api_predict():
    city_code = request.args.get("city", "0")
    crime_code = request.args.get("crime", "9")
    year = request.args.get("year", "2025")
    return jsonify(build_prediction_payload(city_code, crime_code, year))


@app.route("/download-prediction")
def download_prediction():
    payload = build_prediction_payload(
        request.args.get("city", "0"),
        request.args.get("crime", "9"),
        request.args.get("year", "2025"),
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["City", "Crime Type", "Year", "Crime Rate", "Estimated Cases", "Risk Category"])
    writer.writerow(
        [
            payload["city_name"],
            payload["crime_type"],
            payload["year"],
            payload["crime_rate"],
            payload["cases"],
            payload["crime_status"],
        ]
    )
    writer.writerow([])
    writer.writerow(["City Rank", payload["selected_rank"], "of", payload["total_cities"]])
    writer.writerow(["Historical Average", payload["city_average"]])
    writer.writerow(["Difference From Average", payload["average_delta"]])
    writer.writerow([])
    writer.writerow(["Top Risk Cities", "Rate", "Cases"])
    for row in payload["riskiest_cities"]:
        writer.writerow([row["city"], row["rate"], row["cases"]])

    filename = f"crime_prediction_{payload['city_name']}_{payload['year']}.csv".replace(" ", "_")
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/report")
def project_report():
    return send_from_directory(REPORT_DIR, REPORT_FILE, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=False)
