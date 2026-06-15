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


print("HOPEResearch Nutrient Risk Predictor")
print("-----------------------------------")

age = int(input("Age: "))
vegetables = int(input("Vegetable servings per day: "))
meat = int(input("Meat servings per week: "))
dairy = int(input("Dairy servings per week: "))

results = calculate_risk(age, vegetables, meat, dairy)

print("\nEstimated Risk Scores")

for nutrient, score in results.items():
    print(f"{nutrient}: {score}")