import csv
import os
import datetime
import numpy as np

DATA_FILE = "data.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], [], []
    days, scores, texts = [], [], []
    with open(DATA_FILE, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                day = int(float(row[0]))
                score = int(float(row[1]))
                text = row[2].strip('"')
                days.append(day)
                scores.append(score)
                texts.append(text)
    return days, scores, texts

def save_data(day, score, text):
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([day, int(score), text])

def get_month(day_of_year):
    dt = datetime.datetime(datetime.datetime.now().year, 1, 1) + datetime.timedelta(day_of_year - 1)
    return dt.month

def get_season(month):
    if month in [3, 4, 5]:
        return 0
    elif month in [6, 7, 8]:
        return 1
    elif month in [9, 10, 11]:
        return 2
    else:
        return 3

def get_weekday(day_of_year):
    dt = datetime.datetime(datetime.datetime.now().year, 1, 1) + datetime.timedelta(day_of_year - 1)
    return dt.weekday()

def predict_best(target_day, days, scores):
    if not days:
        return None

    m = get_month(target_day)
    s = get_season(m)
    w = get_weekday(target_day)

    # convert features
    target = np.array([m/12.0, s/3.0, w/6.0])

    best_score = None
    best_dist = float("inf")

    for d, sc in zip(days, scores):
        month = get_month(d)
        season = get_season(month)
        weekday = get_weekday(d)
        vec = np.array([month/12.0, season/3.0, weekday/6.0])

        dist = np.linalg.norm(target - vec)  
        if dist < best_dist or (dist == best_dist and sc > best_score):
            best_dist = dist
            best_score = sc

    return best_score

if __name__ == "__main__":
    today = datetime.datetime.now().timetuple().tm_yday

    print("Choose an option:")
    print("1 = Enter day score")
    print("2 = Predict today")
    print("3 = Predict tomorrow")
    print("4 = Predict in (number) days: 4+3 / 4-5")
    choice = input("> ")

    days, scores, texts = load_data()

    if choice == "1":
        score_input = input(f"How good was your day {today} (1-100)? (or type 'skip') ")
        if score_input.strip().lower() != "skip":
            text = input("Describe your day in one word: ")
            save_data(today, score_input, text)
            print("Day saved.")
        else:
            print("Day skipped, nothing saved.")

    elif choice in ["2", "3"]:
        target_day = today if choice == "2" else today + 1
        prediction = predict_best(target_day, days, scores)
        if prediction is not None:
            print(f"Best match for day {target_day}: {prediction}/100")
        else:
            print("No data available to make a prediction!")

    elif choice[0] == "4":
        second_number = int(choice[1:])
        target_day = today + second_number
        prediction = predict_best(target_day, days, scores)
        if prediction is not None:
            print(f"Best match for day {target_day}: {prediction}/100")
        else:
            print("No data available to make a prediction!")
            