import csv
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


def get_risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"


def calculate_risks(age, vegetables, meat, dairy, food_access, supplements):
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

    return (
        get_risk_label(iron_score),
        get_risk_label(b12_score),
        get_risk_label(zinc_score)
    )


def generate_person():
    age = random.randint(5, 18)
    vegetables = random.randint(0, 5)
    meat = random.randint(0, 7)
    dairy = random.randint(0, 7)
    food_access = random.randint(1, 5)
    supplements = random.choice([0, 1])

    iron_risk, b12_risk, zinc_risk = calculate_risks(
        age, vegetables, meat, dairy, food_access, supplements
    )

    return {
        "age": age,
        "vegetables_per_day": vegetables,
        "meat_per_week": meat,
        "dairy_per_week": dairy,
        "food_access": food_access,
        "supplements": supplements,
        "iron_risk": iron_risk,
        "b12_risk": b12_risk,
        "zinc_risk": zinc_risk
    }


def generate_dataset(size):
    people = [generate_person() for _ in range(size)]

    with open("synthetic_population.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=people[0].keys())
        writer.writeheader()
        writer.writerows(people)


def train_model(data, target_column):
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
    report = classification_report(y_test, predictions, zero_division=0)

    return model, accuracy, report


def save_model_report(accuracies, reports):
    with open("model_performance_report.txt", "w") as file:
        file.write("HOPEResearch ML Model Performance Report\n")
        file.write("----------------------------------------\n\n")
        file.write("Important Disclaimer:\n")
        file.write(
            "This is an educational prototype trained on synthetic, rule-generated data. "
            "It is not a diagnostic medical tool and should not be used for clinical decisions.\n\n"
        )

        for nutrient, accuracy in accuracies.items():
            file.write(f"{nutrient} Model Accuracy: {round(accuracy * 100, 2)}%\n")
            file.write("Classification Report:\n")
            file.write(reports[nutrient])
            file.write("\n\n")


generate_dataset(1000)

data = pd.read_csv("synthetic_population.csv")

iron_model, iron_accuracy, iron_report = train_model(data, "iron_risk")
b12_model, b12_accuracy, b12_report = train_model(data, "b12_risk")
zinc_model, zinc_accuracy, zinc_report = train_model(data, "zinc_risk")

accuracies = {
    "Iron": iron_accuracy,
    "Vitamin B12": b12_accuracy,
    "Zinc": zinc_accuracy
}

reports = {
    "Iron": iron_report,
    "Vitamin B12": b12_report,
    "Zinc": zinc_report
}

save_model_report(accuracies, reports)

print("HOPEResearch Multi-Nutrient ML Risk Predictor")
print("---------------------------------------------")
print("Educational prototype trained on synthetic data.")
print("Not for medical diagnosis.\n")

for nutrient, accuracy in accuracies.items():
    print(f"{nutrient} Model Accuracy:", round(accuracy * 100, 2), "%")

example_person = pd.DataFrame([
    {
        "age": 10,
        "vegetables_per_day": 1,
        "meat_per_week": 0,
        "dairy_per_week": 1,
        "food_access": 2,
        "supplements": 0
    }
])

print("\nExample Prediction")
print("------------------")
print("Predicted Iron Risk:", iron_model.predict(example_person)[0])
print("Predicted Vitamin B12 Risk:", b12_model.predict(example_person)[0])
print("Predicted Zinc Risk:", zinc_model.predict(example_person)[0])

print("\nModel performance report saved to model_performance_report.txt")