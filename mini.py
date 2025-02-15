import tweepy
import tkinter as tk
from tkinter import messagebox

# Twitter API credentials (Replace with your own credentials)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Authenticate with Twitter
def authenticate_twitter():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)

twitter_api = authenticate_twitter()

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)
        self.post_to_twitter(workout)

    def view_workouts(self):
        for workout in self.workouts:
            print(workout)

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    date, exercise_type, duration, calories_burned = line.strip().split(',')
                    self.workouts.append(Workout(date, exercise_type, int(duration), int(calories_burned)))
        except FileNotFoundError:
            print("No previous data found.")

    def post_to_twitter(self, workout):
        message = f"Workout Update: {workout.date} - {workout.exercise_type} for {workout.duration} minutes, {workout.calories_burned} calories burned! #FitnessTracker"
        try:
            twitter_api.update_status(message)
            messagebox.showinfo("Success", "Workout update posted to Twitter!")
        except tweepy.TweepError as e:
            messagebox.showerror("Error", f"Error posting to Twitter: {e}")

def add_workout_ui():
    date = date_entry.get()
    exercise_type = exercise_entry.get()
    duration = int(duration_entry.get())
    calories_burned = int(calories_entry.get())
    workout = Workout(date, exercise_type, duration, calories_burned)
    user.add_workout(workout)
    messagebox.showinfo("Success", "Workout added successfully!")

def save_workouts():
    user.save_data("workout_data.txt")
    messagebox.showinfo("Success", "Workout data saved!")

# GUI Setup
user = User("John Doe", 25, 70)
root = tk.Tk()
root.title("Fitness Tracker")
root.geometry("400x300")
root.configure(bg="#ADD8E6")

tk.Label(root, text="Date (YYYY-MM-DD):", bg="#ADD8E6", font=("Arial", 12, "bold")).pack(pady=5)
date_entry = tk.Entry(root, font=("Arial", 12))
date_entry.pack(pady=5)

tk.Label(root, text="Exercise Type:", bg="#ADD8E6", font=("Arial", 12, "bold")).pack(pady=5)
exercise_entry = tk.Entry(root, font=("Arial", 12))
exercise_entry.pack(pady=5)

tk.Label(root, text="Duration (minutes):", bg="#ADD8E6", font=("Arial", 12, "bold")).pack(pady=5)
duration_entry = tk.Entry(root, font=("Arial", 12))
duration_entry.pack(pady=5)

tk.Label(root, text="Calories Burned:", bg="#ADD8E6", font=("Arial", 12, "bold")).pack(pady=5)
calories_entry = tk.Entry(root, font=("Arial", 12))
calories_entry.pack(pady=5)

tk.Button(root, text="Add Workout", command=add_workout_ui, font=("Arial", 12, "bold"), bg="#32CD32", fg="white").pack(pady=5)
tk.Button(root, text="Save Workouts", command=save_workouts, font=("Arial", 12, "bold"), bg="#FF4500", fg="white").pack(pady=5)

tk.mainloop()
