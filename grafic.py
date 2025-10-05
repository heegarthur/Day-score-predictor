import csv
import matplotlib.pyplot as plt

data_file = "data.csv"  

days = []
scores = []
descriptions = []

with open(data_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            day = int(row[0])
            score = float(row[1])
            description = row[2].strip('"')
            
            days.append(day)
            scores.append(score)
            descriptions.append(description)
plt.figure(figsize=(12, 6))
plt.plot(days, scores, marker='o', linestyle='-', color='blue')
plt.title("Score per Day")
plt.xlabel("Day of the Year")
plt.ylabel("Score")
plt.grid(True)
plt.show()
plt.figure(figsize=(12, 6))
plt.bar(days, scores, color='green')
plt.title("Score per Day")
plt.xlabel("Day of the Year")
plt.ylabel("Score")
plt.xticks(days, descriptions, rotation=45, ha='right')
plt.tight_layout()
plt.show()
plt.figure(figsize=(8, 6))
plt.hist(scores, bins=8, color='orange', edgecolor='black')
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Number of Days")
plt.show()
