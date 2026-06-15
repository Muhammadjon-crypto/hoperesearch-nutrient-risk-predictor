import csv
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def get_risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"


def calculate_scores(age, vegetables, meat, dairy, food_access, supplements):
    iron_score = 0
    b12_score = 0
    zinc_score = 0

    if vegetables < 3:
        iron_score += 2

    if meat < 2:
        iron_score += 1
        b12_score += 3
        zinc_score += 2

    if dairy < 2:
        b12_score += 1

    if food_access <= 2:
        iron_score += 2
        b12_score += 1
        zinc_score += 2

    if supplements == 0:
        iron_score += 1
        b12_score += 1
        zinc_score += 1

    if age < 12:
        iron_score += 1
        zinc_score += 1

    return iron_score, b12_score, zinc_score


def calculate_risks(age, vegetables, meat, dairy, food_access, supplements):
    iron_score, b12_score, zinc_score = calculate_scores(
        age, vegetables, meat, dairy, food_access, supplements
    )

    return {
        "iron_risk": get_risk_label(iron_score),
        "b12_risk": get_risk_label(b12_score),
        "zinc_risk": get_risk_label(zinc_score),
    }


def generate_interventions(risks):
    interventions = []

    if risks["iron_risk"] == "High":
        interventions.append("Iron: prioritize beans, spinach, fortified cereals, lean meats, and vitamin C pairing.")
    elif risks["iron_risk"] == "Moderate":
        interventions.append("Iron: increase weekly iron-rich meals and monitor intake.")

    if risks["b12_risk"] == "High":
        interventions.append("B12: consider eggs, dairy, fish, meat, fortified foods, or professional guidance on supplementation.")
    elif risks["b12_risk"] == "Moderate":
        interventions.append("B12: monitor animal-source or fortified-food intake.")

    if risks["zinc_risk"] == "High":
        interventions.append("Zinc: prioritize beans, nuts, seeds, whole grains, meat, and fortified cereals.")
    elif risks["zinc_risk"] == "Moderate":
        interventions.append("Zinc: add more zinc-containing foods throughout the week.")

    if not interventions:
        interventions.append("Overall: current estimated risk is low. Maintain dietary variety.")

    return interventions


def generate_person():
    age = random.randint(5, 18)
    vegetables = random.randint(0, 5)
    meat = random.randint(0, 7)
    dairy = random.randint(0, 7)
    food_access = random.randint(1, 5)
    supplements = random.choice([0, 1])

    risks = calculate_risks(age, vegetables, meat, dairy, food_access, supplements)

    return {
        "age": age,
        "vegetables_per_day": vegetables,
        "meat_per_week": meat,
        "dairy_per_week": dairy,
        "food_access": food_access,
        "supplements": supplements,
        **risks,
    }


def generate_synthetic_population():
    population_size = int(input("Population size: "))
    population = [generate_person() for _ in range(population_size)]

    with open("synthetic_population.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=population[0].keys())
        writer.writeheader()
        writer.writerows(population)

    print("Synthetic population saved to synthetic_population.csv")


def analyze_survey_data():
    filename = input("Enter survey CSV filename: ")
    data = pd.read_csv(filename)

    risk_results = data.apply(
        lambda row: pd.Series(
            calculate_risks(
                row["age"],
                row["vegetables_per_day"],
                row["meat_per_week"],
                row["dairy_per_week"],
                row["food_access"],
                row["supplements"],
            )
        ),
        axis=1,
    )

    final_data = pd.concat([data, risk_results], axis=1)
    final_data.to_csv("analyzed_survey_results.csv", index=False)

    print("Survey responses analyzed:", len(final_data))

    for nutrient in ["iron", "b12", "zinc"]:
        print(f"\n{nutrient.upper()} Risk:")
        print(final_data[f"{nutrient}_risk"].value_counts())

    print("\nAnalyzed results saved to analyzed_survey_results.csv")


def community_dashboard():
    filename = input("Enter analyzed CSV filename: ")
    data = pd.read_csv(filename)

    print("\nHOPEResearch Community Dashboard")
    print("--------------------------------")
    print("Population size:", len(data))

    for nutrient in ["iron", "b12", "zinc"]:
        print(f"\n{nutrient.upper()} Risk Distribution:")
        print(data[f"{nutrient}_risk"].value_counts())


def train_ml_models():
    filename = input("Enter analyzed CSV filename: ")
    data = pd.read_csv(filename)

    features = data[
        [
            "age",
            "vegetables_per_day",
            "meat_per_week",
            "dairy_per_week",
            "food_access",
            "supplements",
        ]
    ]

    for target_column in ["iron_risk", "b12_risk", "zinc_risk"]:
        target = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )

        model = DecisionTreeClassifier(random_state=42, max_depth=5)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        print(f"{target_column} model accuracy:", round(accuracy * 100, 2), "%")

    print("\nDisclaimer: These models are educational prototypes and not diagnostic medical tools.")


def predict_individual_risk():
    age = int(input("Age: "))
    vegetables = int(input("Vegetable servings per day: "))
    meat = int(input("Meat servings per week: "))
    dairy = int(input("Dairy servings per week: "))
    food_access = int(input("Food access score 1-5: "))
    supplements = int(input("Supplements? 1 for yes, 0 for no: "))

    risks = calculate_risks(age, vegetables, meat, dairy, food_access, supplements)
    interventions = generate_interventions(risks)

    print("\nIndividual Nutrient Risk Prediction")
    print("-----------------------------------")
    print("Iron Risk:", risks["iron_risk"])
    print("Vitamin B12 Risk:", risks["b12_risk"])
    print("Zinc Risk:", risks["zinc_risk"])

    print("\nSuggested Interventions")
    print("-----------------------")
    for intervention in interventions:
        print("-", intervention)

    print("\nDisclaimer: Educational screening only. Not medical diagnosis.")


def generate_community_intervention_plan():
    filename = input("Enter analyzed CSV filename: ")
    data = pd.read_csv(filename)

    print("\nHOPEResearch Community Intervention Plan")
    print("----------------------------------------")

    for nutrient in ["iron", "b12", "zinc"]:
        high_count = (data[f"{nutrient}_risk"] == "High").sum()
        moderate_count = (data[f"{nutrient}_risk"] == "Moderate").sum()

        print(f"\n{nutrient.upper()}")
        print("High risk individuals:", high_count)
        print("Moderate risk individuals:", moderate_count)

        if high_count >= 10:
            print("Recommended action: prioritize this nutrient in the next outreach campaign.")
        elif high_count >= 3:
            print("Recommended action: monitor and include targeted educational materials.")
        else:
            print("Recommended action: low immediate priority.")


def generate_community_health_report():
    filename = input("Enter analyzed CSV filename: ")
    data = pd.read_csv(filename)

    report_filename = "community_health_report.txt"

    with open(report_filename, "w") as file:
        file.write("HOPEResearch Community Health Report\n")
        file.write("-----------------------------------\n\n")
        file.write(f"Population analyzed: {len(data)}\n\n")
        file.write("Important Disclaimer:\n")
        file.write("This report is an educational screening prototype, not a medical diagnosis tool.\n\n")

        for nutrient in ["iron", "b12", "zinc"]:
            counts = data[f"{nutrient}_risk"].value_counts()
            high = counts.get("High", 0)
            moderate = counts.get("Moderate", 0)
            low = counts.get("Low", 0)

            high_percent = round((high / len(data)) * 100, 1)
            moderate_percent = round((moderate / len(data)) * 100, 1)
            low_percent = round((low / len(data)) * 100, 1)

            file.write(f"{nutrient.upper()} Deficiency Risk\n")
            file.write(f"- High: {high} ({high_percent}%)\n")
            file.write(f"- Moderate: {moderate} ({moderate_percent}%)\n")
            file.write(f"- Low: {low} ({low_percent}%)\n")

            if high_percent >= 20:
                file.write("Key Finding: High-risk prevalence is elevated and should be prioritized.\n")
                file.write("Recommended Outreach: Focused nutrition education and food-support interventions.\n\n")
            elif high_percent >= 10:
                file.write("Key Finding: Moderate concern level detected.\n")
                file.write("Recommended Outreach: Include this nutrient in educational materials.\n\n")
            else:
                file.write("Key Finding: Lower immediate concern based on current survey data.\n")
                file.write("Recommended Outreach: Continue monitoring.\n\n")

    print(f"Community health report saved to {report_filename}")


def main():
    while True:
        print("\nHOPEResearch Platform")
        print("---------------------")
        print("1. Analyze survey data")
        print("2. Generate synthetic population")
        print("3. Community dashboard")
        print("4. Train ML models")
        print("5. Predict individual nutrient risk")
        print("6. Generate community intervention plan")
        print("7. Generate community health report")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            analyze_survey_data()
        elif choice == "2":
            generate_synthetic_population()
        elif choice == "3":
            community_dashboard()
        elif choice == "4":
            train_ml_models()
        elif choice == "5":
            predict_individual_risk()
        elif choice == "6":
            generate_community_intervention_plan()
        elif choice == "7":
            generate_community_health_report()
        elif choice == "8":
            print("Exiting HOPEResearch Platform.")
            break
        else:
            print("Invalid option.")


main()