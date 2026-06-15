import pandas as pd


def get_risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"


def calculate_risks(row):
    iron_score = 0
    b12_score = 0
    zinc_score = 0

    if row["vegetables_per_day"] < 3:
        iron_score += 2

    if row["meat_per_week"] < 2:
        iron_score += 1
        b12_score += 3
        zinc_score += 2

    if row["dairy_per_week"] < 2:
        b12_score += 1

    if row["food_access"] <= 2:
        iron_score += 2
        b12_score += 1
        zinc_score += 2

    if row["supplements"] == 0:
        iron_score += 1
        b12_score += 1
        zinc_score += 1

    if row["age"] < 12:
        iron_score += 1
        zinc_score += 1

    return pd.Series({
        "iron_risk": get_risk_label(iron_score),
        "b12_risk": get_risk_label(b12_score),
        "zinc_risk": get_risk_label(zinc_score)
    })


data = pd.read_csv("survey_responses.csv")

risk_results = data.apply(calculate_risks, axis=1)

final_data = pd.concat([data, risk_results], axis=1)

final_data.to_csv("analyzed_survey_results.csv", index=False)

print("HOPEResearch Real Survey Risk Analyzer")
print("-------------------------------------")
print("Survey responses analyzed:", len(final_data))

print("\nRisk Summary")

for nutrient in ["iron", "b12", "zinc"]:
    print(f"\n{nutrient.upper()} Risk:")
    print(final_data[f"{nutrient}_risk"].value_counts())

print("\nAnalyzed results saved to analyzed_survey_results.csv")