# Import necessary modules
import tkinter as tk
from tkinter import messagebox
import time
import math
import threading
import pygame
from datetime import datetime, timedelta

# Function to draw the clock
def draw_clock():
    now = time.localtime()
    # Calculate angles for hour, minute, and second hands
    seconds_angle = (90 - now.tm_sec * 6)
    minutes_angle = (90 - (now.tm_min * 6 + now.tm_sec * 0.1))
    hours_angle = (90 - ((now.tm_hour % 12) * 30 + now.tm_min * 0.5))

    # Clear the canvas and draw the clock face
    canvas.delete("all")
    canvas.create_oval(50, 50, 350, 350, outline="darkblue", width=4, fill="lightblue")

    # Draw the hour, minute, and second hands
    draw_hand(hours_angle, length=70, width=6, color="green", style=tk.ROUND)
    draw_hand(minutes_angle, length=110, width=4, color="blue", style=tk.BUTT)
    draw_hand(seconds_angle, length=130, width=2, color="red", style=tk.PROJECTING)

    # Draw clock numbers and lines between numbers
    draw_clock_numbers()
    draw_lines_between_numbers()

    # Schedule the next clock update after 100 milliseconds (0.1 seconds)
    root.after(100, draw_clock)

# Function to draw clock hands
def draw_hand(angle, length, width, color, style):
    angle_rad = math.radians(angle)
    x1 = 200
    y1 = 200
    x2 = x1 + length * math.cos(angle_rad)
    y2 = y1 - length * math.sin(angle_rad)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width, capstyle=style)

# Function to draw clock numbers
def draw_clock_numbers():
    for number in range(1, 13):
        angle = math.radians(90 - number * 30)
        x = 200 + 130 * math.cos(angle)
        y = 200 - 130 * math.sin(angle)
        canvas.create_text(x, y, text=str(number), font=("Comic Sans MS", 16), fill="black")

# Function to draw lines between clock numbers
def draw_lines_between_numbers():
    for number in range(1, 13):
        angle = math.radians(90 - number * 30)
        for _ in range(5):
            x1 = 200 + 140 * math.cos(angle)
            y1 = 200 - 140 * math.sin(angle)
            x2 = 200 + 150 * math.cos(angle)
            y2 = 200 - 150 * math.sin(angle)
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            angle -= math.radians(6)

# Function to set an alarm
def set_alarm():
    # Check if the maximum limit of alarms is reached (5 alarms)
    if len(alarms) >= 5:
        messagebox.showerror("Limit Reached", "More than 5 alarms are not allowed at once.")
        return

    # Get the user-entered alarm date and time strings
    alarm_date_str = entry_alarm_date.get()
    alarm_time_str = entry_alarm_time.get()

    # Validate and process the alarm date and time
    if alarm_date_str and alarm_time_str:
        try:
            alarm_datetime_str = f"{alarm_date_str} {alarm_time_str}"
            alarm_datetime_obj = datetime.strptime(alarm_datetime_str, "%d/%m/%y %H:%M")

            now = datetime.now()

            # Calculate the time difference between the current time and the alarm time
            time_diff = alarm_datetime_obj - now

            # Check if the alarm time is in the future
            if time_diff.total_seconds() <= 0:
                messagebox.showerror("Invalid Alarm Time", "Please enter a future date and time for the alarm.")
                return

            # Add the alarm to the alarms list and start a new thread to handle the alarm
            alarms.append({"datetime": alarm_datetime_obj})
            threading.Thread(target=start_alarm, args=(time_diff, alarm_datetime_obj)).start()

            # Show a success message and clear the input fields
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_datetime_str}")
            entry_alarm_date.delete(0, tk.END)
            entry_alarm_time.delete(0, tk.END)

            # Update the side panel displaying alarms
            update_side_panel()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid date (dd/mm/yy) and time (HH:MM)")

    elif alarm_time_str:
        try:
            now = datetime.now()
            current_date_str = now.strftime("%d/%m/%y")

            alarm_datetime_str = f"{current_date_str} {alarm_time_str}"
            alarm_datetime_obj = datetime.strptime(alarm_datetime_str, "%d/%m/%y %H:%M")

            # If the entered time is before the current time, add one day to the alarm time
            if alarm_datetime_obj <= now:
                alarm_datetime_obj += timedelta(days=1)

            # Calculate the time difference between the current time and the alarm time
            time_diff = alarm_datetime_obj - now

            # Add the alarm to the alarms list and start a new thread to handle the alarm
            alarms.append({"datetime": alarm_datetime_obj})
            threading.Thread(target=start_alarm, args=(time_diff, alarm_datetime_obj)).start()

            # Show a success message and clear the input fields
            messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_datetime_obj.strftime('%d/%m/%y %H:%M')}")
            entry_alarm_date.delete(0, tk.END)
            entry_alarm_time.delete(0, tk.END)

            # Update the side panel displaying alarms
            update_side_panel()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid time (HH:MM)")

    else:
        messagebox.showerror("Invalid Input", "Please enter a valid date (dd/mm/yy) and/or time (HH:MM)")

# Function to start the alarm
def start_alarm(time_diff, alarm_datetime_obj):
    time.sleep(time_diff.total_seconds())

    # Initialize and play the alarm sound using pygame
    pygame.mixer.init()
    pygame.mixer.music.load("Gasolina.mp3")
    pygame.mixer.music.play()

    # Show the alarm message box
    alarm_message_box = messagebox.showinfo("Alarm", "Time to wake up!")

    # Stop the alarm sound
    pygame.mixer.music.stop()

    # Remove the alarm from the alarms list after it's done
    for alarm in alarms:
        if alarm["datetime"] == alarm_datetime_obj:
            alarms.remove(alarm)
            break

    # Update the side panel displaying alarms
    update_side_panel()

# Function to update the digital clock time
def update_digital_time():
    now = datetime.now()
    digital_time_label.config(text=now.strftime("%H:%M:%S"))
    current_date_label.config(text=now.strftime("Date: %d/%m/%y"))

    # Schedule the next update after 1000 milliseconds (1 second)
    root.after(1000, update_digital_time)

# Function to update the side panel displaying alarms
def update_side_panel():
    # Clear the current contents of the side panel
    for widget in side_panel.winfo_children():
        widget.destroy()

    # Add alarms to the side panel with edit and delete buttons
    for i, alarm in enumerate(alarms[:5]):
        alarm_text = f"{i + 1}. {alarm['datetime'].strftime('%H:%M (%d/%m/%y)')}"
        alarm_label = tk.Label(side_panel, text=alarm_text, font=("Comic Sans MS", 12), bg="white")
        alarm_label.grid(row=i, column=0, columnspan=2, pady=5)

        edit_button = tk.Button(side_panel, text="Edit", font=("Comic Sans MS", 10), command=lambda a=alarm: edit_alarm(a), bg="orange")
        edit_button.grid(row=i, column=2, padx=5)

        delete_button = tk.Button(side_panel, text="Delete", font=("Comic Sans MS", 10), command=lambda a=alarm: delete_alarm(a), bg="red")
        delete_button.grid(row=i, column=3, padx=5)

# Function to edit an alarm
def edit_alarm(alarm):
    # Pre-fill the entry fields with the alarm date and time for editing
    entry_alarm_date.delete(0, tk.END)
    entry_alarm_time.delete(0, tk.END)
    entry_alarm_date.insert(0, alarm['datetime'].strftime("%d/%m/%y"))
    entry_alarm_time.insert(0, alarm['datetime'].strftime("%H:%M"))

    # Remove the alarm from the alarms list (it will be added again when the user sets the edited alarm)
    alarms.remove(alarm)

# Function to delete an alarm
def delete_alarm(alarm):
    # Remove the alarm from the alarms list and update the side panel
    alarms.remove(alarm)
    update_side_panel()

# Initialize the tkinter window
root = tk.Tk()
root.title("Alarm Clock")

# Set window dimensions and position it in the center of the screen
window_width = 870
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = (screen_width // 2) - (window_width // 2)
y_pos = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# Create the canvas to draw the clock
canvas = tk.Canvas(root, width=400, height=400, bg="lightgray")
canvas.grid(row=0, column=0, columnspan=4)

# Create labels for digital time and current date
digital_time_label = tk.Label(root, font=("Comic Sans MS", 30, "bold"), fg="navy")
digital_time_label.grid(row=1, column=0, columnspan=4)

current_date_label = tk.Label(root, font=("Comic Sans MS", 18), fg="black")
current_date_label.grid(row=2, column=0, columnspan=4)

# Create input fields for setting alarms
label_instruction_date = tk.Label(root, text="Enter alarm date (dd/mm/yy):", font=("Comic Sans MS", 12))
label_instruction_date.grid(row=3, column=0, columnspan=2, pady=10)

entry_alarm_date = tk.Entry(root, font=("Comic Sans MS", 20))
entry_alarm_date.grid(row=3, column=2, columnspan=2, pady=10)

label_instruction_time = tk.Label(root, text="Enter alarm time (HH:MM):", font=("Comic Sans MS", 12))
label_instruction_time.grid(row=4, column=0, columnspan=2, pady=10)

entry_alarm_time = tk.Entry(root, font=("Comic Sans MS", 20))
entry_alarm_time.grid(row=4, column=2, columnspan=2, pady=10)

# Create the "Set Alarm" button
btn_set_alarm = tk.Button(root, text="Set Alarm", font=("Comic Sans MS", 16), command=set_alarm, bg="green")
btn_set_alarm.grid(row=5, column=0, columnspan=4, pady=10)

# Create "Edit" and "Delete" buttons (Initially hidden in the UI, they will be added to the side panel)
btn_edit_alarm = tk.Button(root, text="Edit", font=("Comic Sans MS", 10), command=edit_alarm, bg="orange")
btn_edit_alarm.grid(row=6, column=1, pady=5)

btn_delete_alarm = tk.Button(root, text="Delete", font=("Comic Sans MS", 10), command=delete_alarm, bg="red")
btn_delete_alarm.grid(row=6, column=2, pady=5)

# Create a side panel to display alarms
side_panel = tk.Frame(root, bg="white", width=180, height=320)
side_panel.grid(row=0, column=4, rowspan=7, padx=10, pady=10)

# Initialize the list to store alarms
alarms = []

# Start drawing the clock, updating the digital time, and displaying the side panel
draw_clock()
root.after(0, update_digital_time)
update_side_panel()

# Start the tkinter main loop
root.mainloop()
