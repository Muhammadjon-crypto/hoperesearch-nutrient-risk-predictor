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


def calculate_risk(age, vegetables, meat, dairy, food_access, supplements):
    iron_risk = 0

    if vegetables < 3:
        iron_risk += 2

    if meat < 2:
        iron_risk += 1

    if food_access <= 2:
        iron_risk += 2

    if supplements == 0:
        iron_risk += 1

    if age < 12:
        iron_risk += 1

    return get_risk_label(iron_risk)


def generate_person():
    age = random.randint(5, 18)
    vegetables = random.randint(0, 5)
    meat = random.randint(0, 7)
    dairy = random.randint(0, 7)
    food_access = random.randint(1, 5)
    supplements = random.choice([0, 1])

    iron_risk = calculate_risk(age, vegetables, meat, dairy, food_access, supplements)

    return {
        "age": age,
        "vegetables_per_day": vegetables,
        "meat_per_week": meat,
        "dairy_per_week": dairy,
        "food_access": food_access,
        "supplements": supplements,
        "iron_risk": iron_risk
    }


def generate_dataset(size):
    people = [generate_person() for _ in range(size)]

    with open("synthetic_population.csv", "w", newline="") as file:
        fieldnames = people[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(people)


generate_dataset(1000)

data = pd.read_csv("synthetic_population.csv")

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

target = data["iron_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    features,
    target,
    test_size=0.2,
    random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("HOPEResearch Machine Learning Nutrient Risk Predictor")
print("----------------------------------------------------")
print("Model trained to predict iron deficiency risk")
print("Accuracy:", round(accuracy * 100, 2), "%")

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

prediction = model.predict(example_person)

print("\nExample Prediction")
print("------------------")
print("Predicted Iron Risk:", prediction[0])