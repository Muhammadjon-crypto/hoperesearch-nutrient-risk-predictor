import csv
import random


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

    return iron_risk, b12_risk, zinc_risk


def generate_person():
    age = random.randint(5, 18)
    vegetables = random.randint(0, 5)
    meat = random.randint(0, 7)
    dairy = random.randint(0, 7)
    food_access = random.randint(1, 5)
    supplements = random.choice(["yes", "no"])

    iron, b12, zinc = calculate_risk(
        age, vegetables, meat, dairy, food_access, supplements
    )

    return {
        "age": age,
        "vegetables_per_day": vegetables,
        "meat_per_week": meat,
        "dairy_per_week": dairy,
        "food_access": food_access,
        "supplements": supplements,
        "iron_score": iron,
        "iron_risk": get_risk_label(iron),
        "b12_score": b12,
        "b12_risk": get_risk_label(b12),
        "zinc_score": zinc,
        "zinc_risk": get_risk_label(zinc)
    }


def generate_population(size):
    population = []

    for _ in range(size):
        person = generate_person()
        population.append(person)

    return population


def save_population_csv(population):
    with open("synthetic_population.csv", "w", newline="") as file:
        fieldnames = [
            "age",
            "vegetables_per_day",
            "meat_per_week",
            "dairy_per_week",
            "food_access",
            "supplements",
            "iron_score",
            "iron_risk",
            "b12_score",
            "b12_risk",
            "zinc_score",
            "zinc_risk"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(population)


def count_high_risk(population, nutrient):
    risk_key = nutrient + "_risk"
    count = 0

    for person in population:
        if person[risk_key] == "High":
            count += 1

    return count


population_size = 1000
population = generate_population(population_size)

save_population_csv(population)

iron_high = count_high_risk(population, "iron")
b12_high = count_high_risk(population, "b12")
zinc_high = count_high_risk(population, "zinc")

print("HOPEResearch Synthetic Population Analysis")
print("-----------------------------------------")
print("Population size:", population_size)
print("High Iron Risk:", iron_high)
print("High Vitamin B12 Risk:", b12_high)
print("High Zinc Risk:", zinc_high)
print("\nDataset saved to synthetic_population.csv")