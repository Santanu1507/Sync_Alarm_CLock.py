# Alarm Clock Application

This is a simple Alarm Clock application with a graphical user interface (GUI) built using Python and the Tkinter library. The application allows users to set multiple alarms and visualize the current time with clock hands on the canvas.

## Features

- Set multiple alarms with dates and times.
- Edit and delete existing alarms.
- Visualize the current time with hour, minute, and second hands on the canvas.

## Requirements

- Python 3.x
- Tkinter library (usually comes pre-installed with Python)
- Pygame library (used for playing alarm sound)

## Usage

1. Run the `alarm_clock.py` file to start the application.
2. Enter the alarm date (dd/mm/yy) and time (HH:MM) in the respective input fields.
3. Click the "Set Alarm" button to set the alarm.
4. The application will display the set alarms on the right side of the window.
5. To edit or delete an alarm, click the "Edit" or "Delete" button next to the alarm in the list.
6. The clock visualization will show the current time with hour, minute, and second hands rotating.

## How It Works

The application uses the Tkinter library to create a graphical interface with input fields, buttons, and a canvas for drawing the clock. It also utilizes the Pygame library to play an alarm sound when the set alarm time is reached.

The `draw_clock()` function is responsible for drawing the clock on the canvas and updating the clock hands every second. The `draw_hand()` function calculates the coordinates of the clock hands based on the current time.

The `set_alarm()` function handles setting alarms. It validates the user input for the alarm date and time and adds the alarm to the `alarms` list. The `start_alarm()` function runs in a separate thread and plays the alarm sound when the alarm time is reached.

The `update_digital_time()` function updates the digital clock time displayed on the window every second. The `update_side_panel()` function updates the list of alarms displayed on the side panel.

## Future Improvements

- Allow users to choose a different alarm sound.
- Implement a snooze feature for the alarm.
- Improve the UI design and add more customization options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
