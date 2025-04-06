'''
@author: PythonDeveloper29042
@project: AutoShutdown 
@file: controller.py
@file-description: This file is the controller of the application. It is responsible for the communication between the model and the view.
'''

from datetime import datetime, timedelta
from tkinter import messagebox
from threading import Thread
from time import sleep
import model

count_secs = None  # Variable to store the number of seconds
running = False  # Variable to store the running state of the countdown


def shutdown_model(time: datetime, **countdown_data):
    '''
    This function is responsible for shutting down the system at the specified model time.
    Args:
        time (datetime): The time at which the system should be shut down.
        **countdown_data: The data required for the countdown.
    '''
    global running, count_secs  # Get the global variable running and count_secs
    # Check if the time is empty or not
    if time.strip() == '':
        messagebox.showerror('Error', 'Please select a valid time!')  # Show error message if time is empty
        return
    current_time = datetime.now()  # Get the current time
    if 's' in time:  # Check if the time contains 's' ('seconds')
        future_time = timedelta(seconds=int(time[:-2]))  # Get the future time in seconds
    if 'min' in time:  # Check if the time contains 'min' ('minutes')
        future_time = timedelta(minutes=int(time[:-3]))  # Get the future time in minutes
    if 'hr' in time:  # Check if the time contains 'hr' ('hours')
        future_time = timedelta(hours=int(time[:-3]))  # Get the future time in hours
    current_time += future_time  # Add the future time to the current time        
    running = True  # Set the running state to True
    count_secs = future_time.total_seconds()  # Get the total number of seconds


    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    countdown_data['end_time'].set(f'The system will shut down in:\n{year}/{month:02d}/{day:02} {hour:02d}:{minute:02d}:{second:02d}')
    th = Thread(target=countdown, args=(countdown_data,))  # Create a new thread for the countdown function
    th.start()  # Start the thread


def shutdown_custom(time: datetime, **countdown_data):
    '''
    This function is responsible for shutting down the system at the specified custom time.
    Args:
        time (datetime): The time at which the system should be shut down.
        **countdown_data: The data required for the countdown.
    '''
    global running, count_secs  # Get the global variable running and count_secs
    # print(time, countdown_data)  # Print the time and countdown data for debugging purposes
    current_time = datetime.now()  # Get the current time
    if time <= current_time:  # Check if the selected time is in the past
        messagebox.showerror('Error', 'The selected time is in the past! You can only select future time!')  # Show error message if the selected time is in the past
        return
    count_secs = (time - current_time).total_seconds()  # Calculate the total number of seconds
    running = True  # Set the running state to True

    # current_time = datetime.now()  # Get the current time
    # if '秒' in time:  # Check if the time contains '秒' ('seconds')
    #     future_time = timedelta(seconds=int(time[:-1]))  # Get the future time in seconds
    # if '分钟' in time:  # Check if the time contains '分钟' ('minutes')
    #     future_time = timedelta(minutes=int(time[:-2]))  # Get the future time in minutes
    # if '小时' in time:  # Check if the time contains '小时' ('hours')
    #     future_time = timedelta(hours=int(time[:-2]))  # Get the future time in hours
    # current_time += future_time  # Add the future time to the current time        
    # running = True  # Set the running state to True
    # count_secs = future_time.total_seconds()  # Get the total number of seconds

    countdown_data['end_time'].set(f'The system will shut down in:\n{time.year}/{time.month:02d}/{time.day:02d} {time.hour:02d}:{time.minute:02d}:{time.second:02d}')  # Set the end time in the countdown data
    th = Thread(target=countdown, args=(countdown_data,))  # Create a new thread for the countdown function
    th.start()  # Start the thread
    countdown_data["callback"]()


def cancel_shutdown():
    '''
    This function is responsible for cancelling the scheduled shutdown.
    '''
    global running  # Get the global variable running
    running = False  # Set the running state to False
    messagebox.showinfo('Cancellation', 'The shutdown has been cancelled!')  # Show a message box to inform the user that the shutdown has been cancelled



def change_time():
    '''
    This function is responsible for changing the time at which the system should be shut down.
    '''
    pass


def countdown(countdown_data):
    '''
    This function is responsible for the countdown to the shutdown of the system.
    '''
    global count_secs  # Get the global variable count_secs
    while running:
        if count_secs <= 0:  # Check if the countdown has reached 0
            model.send_shutdown()  # Send the shutdown signal to the model
            break
        count_secs -= 1  # Decrement the number of seconds
        temp = count_secs  # Store the number of seconds in a temporary variable
        hour = int(temp // 3600)  # Calculate the number of hours
        temp %= 3600  # Get the remaining seconds
        minute = int(temp // 60)  # Calculate the number of minutes
        minute %= 60  # Get the remaining minutes
        seconds = int(temp)  # Calculate the number of seconds
        seconds %= 60  # Get the remaining seconds
        countdown_data['count_time'].set(f'{hour:02d}:{minute:02d}:{seconds:02d}')  # Update the countdown window with the remaining time
        sleep(1)  # Sleep for 1 second
    