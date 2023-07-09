# Exercise Reminder

This is a simple exercise reminder application built using Tkinter in Python.

## Functionality

The application allows you to select exercises from a dropdown menu and keeps track of your exercise sets and time. Here are the main features:

- Select an exercise from the dropdown menu.
- Each exercise has a specific number of sets and time duration.
- The application starts a timer for the selected exercise.
- After completing a set, click the "Complete Set" button to move to the next set or exercise.
- The application keeps track of completed sessions and displays the progress using a progress bar.
- You can view the sessions log to see the details of your exercise sessions.
- The sessions log is saved to a CSV file named `ExercisesMMDDYYYY.csv`, where MMDDYYYY represents the current date.

## Requirements

- Python 3.x
- Tkinter module
- pytz module
- csv module

## How to Run

1. Install the required modules mentioned above.
2. Clone the repository or download the `exercise_reminder.py` file.
3. Open a terminal or command prompt and navigate to the directory where the `exercise_reminder.py` file is located.
4. Run the following command:

   ```shell
   python exercise_reminder.py

The application window will appear, and you can start using the exercise reminder.

## Note
The application is currently set to the "America/Denver" timezone (MST). You can modify this by changing the mst_timezone variable in the code.
The application is designed to track 8 exercise sessions in total.
