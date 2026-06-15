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
        "zinc_risk": get_risk_label(zinc_score)
    }


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
        **risks
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
                row["supplements"]
            )
        ),
        axis=1
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
            "supplements"
        ]
    ]

    for target_column in ["iron_risk", "b12_risk", "zinc_risk"]:
        target = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=0.2,
            random_state=42
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

    print("\nIndividual Nutrient Risk Prediction")
    print("-----------------------------------")
    print("Iron Risk:", risks["iron_risk"])
    print("Vitamin B12 Risk:", risks["b12_risk"])
    print("Zinc Risk:", risks["zinc_risk"])
    print("\nDisclaimer: Educational screening only. Not medical diagnosis.")


def main():
    while True:
        print("\nHOPEResearch Platform")
        print("---------------------")
        print("1. Analyze survey data")
        print("2. Generate synthetic population")
        print("3. Community dashboard")
        print("4. Train ML models")
        print("5. Predict individual nutrient risk")
        print("6. Exit")

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
            print("Exiting HOPEResearch Platform.")
            break
        else:
            print("Invalid option.")


main()