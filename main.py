def get_risk_label(score):
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Moderate"
    else:
        return "Low"


def calculate_risk(age, vegetables, meat, dairy):
    iron_risk = 0
    b12_risk = 0
    zinc_risk = 0

    if vegetables < 3:
        iron_risk += 2

    if meat < 2:
        iron_risk += 1
        b12_risk += 3
        zinc_risk += 2

    if dairy < 2:
        b12_risk += 1

    if age < 12:
        iron_risk += 1

    return {
        "Iron Deficiency": iron_risk,
        "Vitamin B12 Deficiency": b12_risk,
        "Zinc Deficiency": zinc_risk
    }


def save_report(results):
    with open("nutrient_report.txt", "w") as file:
        file.write("HOPEResearch Nutrient Risk Report\n")
        file.write("---------------------------------\n\n")

        for nutrient, score in results.items():
            label = get_risk_label(score)
            file.write(f"{nutrient}: {score} ({label} Risk)\n")


def save_csv(results):
    with open("risk_results.csv", "w") as file:
        file.write("nutrient,score,risk_level\n")

        for nutrient, score in results.items():
            label = get_risk_label(score)
            file.write(f"{nutrient},{score},{label}\n")


print("HOPEResearch Nutrient Risk Predictor")
print("-----------------------------------")

age = int(input("Age: "))
vegetables = int(input("Vegetable servings per day: "))
meat = int(input("Meat servings per week: "))
dairy = int(input("Dairy servings per week: "))

results = calculate_risk(age, vegetables, meat, dairy)

print("\nEstimated Risk Scores")

for nutrient, score in results.items():
    label = get_risk_label(score)
    print(f"{nutrient}: {score} ({label} Risk)")

save_report(results)
save_csv(results)

print("\nReport saved to nutrient_report.txt")
print("CSV saved to risk_results.csv")