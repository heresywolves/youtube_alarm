import datetime
from msilib.schema import Error
import os
import time
import random
import webbrowser
from tkinter import *
import threading

# If video URL file does not exist, create one
if not os.path.isfile('youtube_alarm_videos.txt'):
    print('Creating "youtube_alarm_videos.txt"...')
with open('youtube_alarm_videos.txt', 'w') as alarm_file:
    alarm_file.write('https://www.youtube.com/watch?v=PUf9_1jsCyY')

# Checks to see if the user has entered in a valid alarm time


def check_alarm_input(alarm_time):
    if len(alarm_time) == 1:  # [Hour] Format
        if alarm_time[0] < 24 and alarm_time[0] >= 0:
            return True

    elif len(alarm_time) == 2:  # [Hour:Minute] Format
        if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
                alarm_time[1] < 60 and alarm_time[1] >= 0:
            return True

    elif len(alarm_time) == 3:  # [Hour:Minute:Second] Format
        if alarm_time[0] < 24 and alarm_time[0] >= 0 and \
            alarm_time[1] < 60 and alarm_time[1] >= 0 and \
                alarm_time[2] < 60 and alarm_time[2] >= 0:
            return True
    else:
        return False


def set_alarm():
    global entry
    global output_text

    alarm_time = str(entry.get())

    # Get user input and check if it's correct
    while True:

        try:
            alarm_time = [int(n) for n in alarm_time.split(":")]
            if check_alarm_input(alarm_time):

                # Convert the alarm time from [H:M] or [H:M:S] to seconds
                # Number of seconds in an Hour, Minute, and Second
                seconds_hms = [3600, 60, 1]
                alarm_seconds = sum(
                    [a*b for a, b in zip(seconds_hms[:len(alarm_time)], alarm_time)])

                # Get the current time of day in seconds
                now = datetime.datetime.now()
                current_time_seconds = sum(
                    [a*b for a, b in zip(seconds_hms, [now.hour, now.minute, now.second])])

                # Calculate the number of seconds until alarm goes off
                time_diff_seconds = alarm_seconds - current_time_seconds

                # If time difference is negative, set alarm for next day
                if time_diff_seconds < 0:
                    time_diff_seconds += 86400  # Number of seconds in a day

                # Display the amount of time until alarm goes off
                set_time = str('Alarm set to go off in %s' %
                               datetime.timedelta(seconds=time_diff_seconds))
                output_text.set(set_time)

                # Initiating the alarm in a separate deamon thread
                x = threading.Thread(target=running_alarm,
                                     args=(time_diff_seconds,), daemon=True)
                x.start()

                break

            else:
                output_text.set(
                    'ERROR: Please enter time in the correct format')
                break
        except:
            output_text.set('ERROR: Please enter time in the correct format')
            break


def running_alarm(time_diff_seconds):
    global output_text

    # Sleep until the alarm goes off
    print(f'Seconds until the alarm goes off {time_diff_seconds}')
    time.sleep(time_diff_seconds)

    # Alarm goes off
    output_text.set('Wake up!')

    # Load list of possible video URLs
    with open('youtube_alarm_videos.txt', 'r') as alarm_file:
        videos = alarm_file.readlines()

    # Open a random video from the list
    return webbrowser.open(random.choice(videos))


if __name__ == "__main__":

    # GUI initialization
    gui = Tk()
    gui.title('YouTube')
    gui.geometry('400x350')
    gui.configure(bg='black')
    gui.resizable(False, False)

    # Images and icons
    icon = PhotoImage(file='GUI\\icon.png')
    gui.iconphoto(True, icon)

    # Text with instructions
    instructions = Label(
        gui, text='Set a time for the alarm (Ex. 06:30 or 18:30:00)',
        font=('calibre', 12, 'bold'), background='black', fg='white', justify=CENTER)
    instructions.grid(row=1, column=1, ipady=20, ipadx=20)

    # Entry field
    entry = Entry(gui, bg='#191818', fg='white',
                  borderwidth=1, highlightthickness=1, width=10)
    entry.grid(row=2, column=1)

    # Set Button
    set_button = Button(gui, bg='gray', text='SET ALARM', fg='white', activebackground="green", anchor='center',
                        borderwidth=0, highlightthickness=0, command=lambda: set_alarm())
    set_button.grid(row=3, column=1)

    # Program output field
    output_text = StringVar()
    output_label = Label(gui, textvariable=output_text,
                         font=('calibre', 10, 'bold'), background='black', fg='white')
    output_label.grid(row=4, column=1, pady=50)

    # Execute tkinter
    gui.mainloop()
