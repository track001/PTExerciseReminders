import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import time


class ExerciseReminder:

  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Exercise Reminder")
    self.root.geometry("300x300")

    self.current_exercise = None
    self.current_set = None
    self.remaining_time = 0
    self.session_count = 0
    self.sessions_log = []

    self.exercises = {
      "Knee Extension": {
        "sets": 3,
        "time": 30
      },
      "Knee Flexion": {
        "sets": 3,
        "time": 30
      },
      "Single Leg Stand": {
        "sets": 1,
        "time": 60
      }
    }

    self.exercise_label = tk.Label(self.root, text="Select Exercise:")
    self.exercise_label.pack()

    self.exercise_var = tk.StringVar(self.root)
    self.exercise_dropdown = ttk.Combobox(self.root,
                                          textvariable=self.exercise_var,
                                          state="readonly")
    self.exercise_dropdown["values"] = list(self.exercises.keys())
    self.exercise_dropdown.bind("<<ComboboxSelected>>", self.start_exercise)
    self.exercise_dropdown.pack()

    self.sets_count_label = tk.Label(self.root, text="")
    self.sets_count_label.pack()

    self.timer_label = tk.Label(self.root, text="Timer: ")
    self.timer_label.pack()

    self.complete_button = tk.Button(self.root,
                                     text="Complete Set",
                                     state=tk.DISABLED,
                                     command=self.complete_set)
    self.complete_button.pack()

    self.session_info_label = tk.Label(self.root, text="")
    self.session_info_label.pack()

    self.progress_bar = ttk.Progressbar(self.root,
                                        orient="horizontal",
                                        length=200,
                                        mode="determinate")
    self.progress_bar.pack()

    self.average_sessions_label = tk.Label(self.root, text="")
    self.average_sessions_label.pack()

    self.view_sessions_button = tk.Button(self.root,
                                          text="View Sessions",
                                          command=self.view_sessions)
    self.view_sessions_button.pack()

    self.add_session_button = tk.Button(self.root,
                                        text="Add Session",
                                        command=self.add_session)
    self.add_session_button.pack()

    self.edit_session_button = tk.Button(self.root,
                                         text="Edit Session Log",
                                         command=self.edit_session_log)
    self.edit_session_button.pack()

    self.save_log_button = tk.Button(self.root,
                                     text="Save Session Log",
                                     command=self.save_session_log)
    self.save_log_button.pack()

    self.upload_log_button = tk.Button(self.root,
                                       text="Upload Session Logs",
                                       command=self.upload_session_logs)
    self.upload_log_button.pack()

    self.check_session_count()
    self.check_timer()

    self.root.mainloop()

  def start_exercise(self, event):
    exercise = self.exercise_var.get()
    self.current_exercise = exercise
    self.current_set = 1
    self.remaining_time = self.exercises[exercise]["time"]
    self.sets_count_label.configure(
      text=
      f"{exercise}: Set {self.current_set} of {self.exercises[exercise]['sets']} sets"
    )
    self.timer_label.configure(
      text=f"Timer: {self.remaining_time//60:02d}:{self.remaining_time%60:02d}"
    )
    self.complete_button.configure(state=tk.NORMAL)

  def complete_set(self):
    exercise = self.current_exercise
    if self.current_set < self.exercises[exercise]["sets"]:
      self.current_set += 1
      self.remaining_time = self.exercises[exercise]["time"]
      self.sets_count_label.configure(
        text=
        f"{exercise}: Set {self.current_set} of {self.exercises[exercise]['sets']} sets"
      )
      self.timer_label.configure(
        text=
        f"Timer: {self.remaining_time//60:02d}:{self.remaining_time%60:02d}")
    else:
      self.current_exercise = None
      self.sets_count_label.configure(text="")
      self.timer_label.configure(text="Timer: ")
      self.complete_button.configure(state=tk.DISABLED)
      self.session_count += 1
      self.sessions_log.append(time.strftime("%H:%M"))
      self.check_session_count()

  def check_timer(self):
    if self.current_exercise is not None and self.remaining_time > 0:
      self.remaining_time -= 1
      self.timer_label.configure(
        text=
        f"Timer: {self.remaining_time//60:02d}:{self.remaining_time%60:02d}")
    self.root.after(1000, self.check_timer)

  def check_session_count(self):
    self.session_info_label.configure(
      text=f"Sessions completed: {self.session_count}/8")
    if self.session_count == 8:
      self.session_info_label.configure(foreground="green")
    else:
      self.session_info_label.configure(foreground="black")

  def view_sessions(self):
    if not self.sessions_log:
      messagebox.showwarning("View Sessions", "No sessions available to view.")
      return

    sessions_message = "Sessions Log:\n"
    for i, session_time in enumerate(self.sessions_log, start=1):
      sessions_message += f"Session {i}: {session_time}\n"

    messagebox.showinfo("View Sessions", sessions_message)

  def add_session(self):
    num_sessions = simpledialog.askinteger(
      "Add Session", "Enter the number of sessions to add:")
    if num_sessions:
      self.session_count += num_sessions
      for _ in range(num_sessions):
        self.sessions_log.append(time.strftime("%H:%M"))
      self.check_session_count()

  def edit_session_log(self):
    if not self.sessions_log:
      messagebox.showwarning("Edit Session Log",
                             "No sessions available to edit.")
      return

    selected_session = simpledialog.askinteger(
      "Edit Session Log", "Enter the session number to edit:")
    if selected_session:
      selected_session_index = selected_session - 1
      if selected_session_index < len(self.sessions_log):
        edited_time = simpledialog.askstring(
          "Edit Session Log",
          "Enter the new session time (HH:MM):",
          initialvalue=self.sessions_log[selected_session_index])
        if edited_time:
          self.sessions_log[selected_session_index] = edited_time
          self.check_session_count()
      else:
        messagebox.showwarning(
          "Edit Session Log",
          "Invalid session number. Please select a valid session to edit.")

  def save_session_log(self):
    if not self.sessions_log:
      messagebox.showwarning("Save Session Log",
                             "No sessions available to save.")
      return

    filename = "session_log.csv"
    with open(filename, mode="w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["Session Time"])
      writer.writerows([[session_time] for session_time in self.sessions_log])
    messagebox.showinfo("Save Session Log",
                        f"Session log saved as '{filename}'.")

  def upload_session_logs(self):
    filename = simpledialog.askstring("Upload Session Logs",
                                      "Enter the filename to upload:")
    if filename:
      try:
        with open(filename, mode="r") as file:
          reader = csv.reader(file)
          session_times = [row[0] for row in reader]
          self.sessions_log.extend(session_times)
          self.session_count += len(session_times)
          self.check_session_count()
          messagebox.showinfo("Upload Session Logs",
                              "Session logs uploaded successfully.")
      except FileNotFoundError:
        messagebox.showwarning(
          "Upload Session Logs",
          "File not found. Please enter a valid filename.")
      except csv.Error:
        messagebox.showwarning("Upload Session Logs",
                               "Error occurred while reading the CSV file.")


if __name__ == "__main__":
  ExerciseReminder()
