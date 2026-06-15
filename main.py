import csv
import random
import matplotlib.pyplot as plt


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

    iron, b12, zinc = calculate_risk(age, vegetables, meat, dairy, food_access, supplements)

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
    return [generate_person() for _ in range(size)]


def save_population_csv(population):
    with open("synthetic_population.csv", "w", newline="") as file:
        fieldnames = list(population[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(population)


def summarize_risk_levels(population, nutrient):
    risk_key = nutrient + "_risk"

    summary = {
        "High": 0,
        "Moderate": 0,
        "Low": 0
    }

    for person in population:
        summary[person[risk_key]] += 1

    return summary


def save_dashboard_report(population, summaries):
    with open("community_dashboard_report.txt", "w") as file:
        file.write("HOPEResearch Community Nutrient Risk Dashboard\n")
        file.write("---------------------------------------------\n\n")
        file.write(f"Population size: {len(population)}\n\n")

        for nutrient, summary in summaries.items():
            file.write(nutrient.title() + " Deficiency Risk:\n")
            file.write(f"High Risk: {summary['High']}\n")
            file.write(f"Moderate Risk: {summary['Moderate']}\n")
            file.write(f"Low Risk: {summary['Low']}\n\n")


def save_dashboard_csv(summaries):
    with open("community_dashboard.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["nutrient", "risk_level", "count"])

        for nutrient, summary in summaries.items():
            for risk_level, count in summary.items():
                writer.writerow([nutrient, risk_level, count])


def save_dashboard_plot(summaries):
    nutrients = list(summaries.keys())
    high_counts = [summaries[nutrient]["High"] for nutrient in nutrients]
    moderate_counts = [summaries[nutrient]["Moderate"] for nutrient in nutrients]
    low_counts = [summaries[nutrient]["Low"] for nutrient in nutrients]

    x_positions = range(len(nutrients))

    plt.figure(figsize=(9, 5))
    plt.bar(x_positions, high_counts, label="High")
    plt.bar(x_positions, moderate_counts, bottom=high_counts, label="Moderate")

    low_bottoms = [
        high_counts[i] + moderate_counts[i]
        for i in range(len(nutrients))
    ]

    plt.bar(x_positions, low_counts, bottom=low_bottoms, label="Low")

    plt.title("Community Nutrient Risk Distribution")
    plt.xlabel("Nutrient")
    plt.ylabel("Number of Individuals")
    plt.xticks(x_positions, [nutrient.title() for nutrient in nutrients])
    plt.legend()
    plt.tight_layout()
    plt.savefig("community_dashboard_plot.png")


population_size = 1000
population = generate_population(population_size)

save_population_csv(population)

summaries = {
    "iron": summarize_risk_levels(population, "iron"),
    "b12": summarize_risk_levels(population, "b12"),
    "zinc": summarize_risk_levels(population, "zinc")
}

print("HOPEResearch Community Nutrient Risk Dashboard")
print("---------------------------------------------")
print("Population size:", population_size)

for nutrient, summary in summaries.items():
    print(f"\n{nutrient.title()} Deficiency Risk:")
    print("High Risk:", summary["High"])
    print("Moderate Risk:", summary["Moderate"])
    print("Low Risk:", summary["Low"])

save_dashboard_report(population, summaries)
save_dashboard_csv(summaries)
save_dashboard_plot(summaries)

print("\nDataset saved to synthetic_population.csv")
print("Dashboard report saved to community_dashboard_report.txt")
print("Dashboard CSV saved to community_dashboard.csv")
print("Dashboard plot saved to community_dashboard_plot.png")