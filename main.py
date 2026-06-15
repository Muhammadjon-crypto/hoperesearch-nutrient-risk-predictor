def get_risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"


def calculate_risk(age, vegetables, meat, dairy, food_access, supplements):
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

    if food_access <= 2:
        iron_risk += 2
        b12_risk += 1
        zinc_risk += 2

    if supplements == "no":
        iron_risk += 1
        b12_risk += 1
        zinc_risk += 1

    if age < 12:
        iron_risk += 1
        zinc_risk += 1

    return {
        "Iron Deficiency": iron_risk,
        "Vitamin B12 Deficiency": b12_risk,
        "Zinc Deficiency": zinc_risk
    }


def generate_recommendations(results):
    recommendations = {}

    for nutrient, score in results.items():
        label = get_risk_label(score)

        if nutrient == "Iron Deficiency":
            if label == "High":
                recommendations[nutrient] = "Increase iron-rich foods such as beans, spinach, fortified cereals, lean meats, and pair plant iron with vitamin C foods."
            elif label == "Moderate":
                recommendations[nutrient] = "Monitor iron intake and add more iron-rich meals during the week."
            else:
                recommendations[nutrient] = "Current estimated iron risk is low."

        elif nutrient == "Vitamin B12 Deficiency":
            if label == "High":
                recommendations[nutrient] = "Consider more B12 sources such as eggs, dairy, fish, meat, fortified foods, or speak with a healthcare professional about supplementation."
            elif label == "Moderate":
                recommendations[nutrient] = "Monitor B12 intake, especially if animal-source foods are limited."
            else:
                recommendations[nutrient] = "Current estimated B12 risk is low."

        elif nutrient == "Zinc Deficiency":
            if label == "High":
                recommendations[nutrient] = "Increase zinc-rich foods such as meat, beans, nuts, seeds, whole grains, and fortified cereals."
            elif label == "Moderate":
                recommendations[nutrient] = "Add more zinc-containing foods throughout the week."
            else:
                recommendations[nutrient] = "Current estimated zinc risk is low."

    return recommendations


def save_report(results, recommendations):
    with open("nutrient_report.txt", "w") as file:
        file.write("HOPEResearch Nutrient Risk Report\n")
        file.write("---------------------------------\n\n")

        for nutrient, score in results.items():
            label = get_risk_label(score)
            file.write(f"{nutrient}: {score} ({label} Risk)\n")
            file.write(f"Recommendation: {recommendations[nutrient]}\n\n")


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
food_access = int(input("Food access score from 1 to 5, where 1 is very limited and 5 is strong: "))
supplements = input("Do you take vitamins or supplements? yes/no: ").strip().lower()

results = calculate_risk(age, vegetables, meat, dairy, food_access, supplements)
recommendations = generate_recommendations(results)

print("\nEstimated Risk Scores")

for nutrient, score in results.items():
    label = get_risk_label(score)
    print(f"{nutrient}: {score} ({label} Risk)")
    print(f"Recommendation: {recommendations[nutrient]}\n")

save_report(results, recommendations)
save_csv(results)

print("Report saved to nutrient_report.txt")
print("CSV saved to risk_results.csv")