from psychopy import visual, core, event, gui, prefs
import csv
import os
import numpy as np
import datetime # To account for time of day

prefs.hardware['audioLib'] = ['pygame']  # or ['sounddevice', 'pyo']
from psychopy import sound #Importing sound after library specification is paramount for code stability

# Try initializing sound
try:
    metronome = sound.Sound(value='A', secs=0.1)
except Exception as e:
    print(f"Error initializing metronome sound: {e}")

# Task and Frequency Selection Dialog
task_dialog = gui.Dlg(title="Task and Frequency Selection")
task_dialog.addField("Choose task type:", choices=["Visual Pulsation", "Metronome", "Both"])
task_dialog.addField("Choose frequency:", choices=["Fast", "Slow"])
task_dialog.show()

if task_dialog.OK:
    task_type = task_dialog.data[0]
    frequency_choice = task_dialog.data[1]
else:
    core.quit()  # Exit if dialog is canceled

# Set beat interval based on frequency choice
if frequency_choice == "Fast":
    beat_interval = 0.4  # 400ms for fast
    offset = 0.1 #Offset to use to syncronise circle pulsation and auditory one
else:
    beat_interval = 0.8  # 800ms for slow
    offset = 0.7 #Offset for slow beat

# Participant Info Dialog
participant_dialog = gui.Dlg(title="Participant Info")
participant_dialog.addField("Participant ID:")
participant_dialog.addField("Participant age:")
participant_dialog.addField("What is your gender?", choices=["Woman", "Non-Binary", "Man"])
participant_dialog.addField("Write the name of your country of Origin")
participant_dialog.addField("Write the name of your native language, in case of bilinguism: the language you use most often.")
participant_dialog.addField("Do you regularly play an instrument or sing?", choices=["Yes", "No"])
participant_dialog.addField("Write the number of years of formal musical training you have received:")
participant_dialog.addField("Did you start your formal musical education before the age of 7?", choices=["Yes", "No"])
participant_dialog.show()

if participant_dialog.OK:
    participant_id = participant_dialog.data[0]
    participant_age = participant_dialog.data[1]
    participant_gender = participant_dialog.data[2]
    participant_country = participant_dialog.data[3]
    participant_language = participant_dialog.data[4]
    musical_experience = participant_dialog.data[5]
    formal_education = participant_dialog.data[6]
    early_trained = participant_dialog.data[7]
else:
    core.quit()  # Exit if dialog is canceled

# Define fullscreen window
win = visual.Window(color=[-1, -1, -1], units="pix", fullscr=True)

# Consent Dialog
consent_text = visual.TextStim(win, text="If you are sensitive to rapidly flashing lights, this experiment might bother you, otherwise it poses no risks.\n\nYour anonymised data will be used for a research paper.\n\nPress 'space' to consent to participate or 'escape' to exit.",
                               color="white", height=40, wrapWidth=800)
consent_text.draw()
win.flip()

# Wait for participant to either consent or exit
keys = event.waitKeys(keyList=['space', 'escape'])

if 'escape' in keys:
    print("Participant chose to exit.")
    win.close()
    core.quit()  # Exit if 'escape' is pressed
elif 'space' in keys:
    print("Participant consented.")
    # Proceed to the experiment
    

# Define text stimuli
instruction_text = visual.TextStim(win, text="Tap the spacebar with one finger to the beat you feel.\n\nPress 'space' to start.", 
                                   color="white", height=40, wrapWidth=800)
pause_text = visual.TextStim(win, text="You will be now presented with a stimulus.\n\nDo not tap any key.\n\nFeel free to move though!",
                                    color="white", height=40, wrapWidth=800)
pause2_text = visual.TextStim(win, text="Now verbally describe the picture shown.\n\n Take your time and, once done, press the right arrow to progress to the next. Take as long as you want.",
                                    color="white", height=40, wrapWidth=800)   
instruction2_text = visual.TextStim(win, text="Now again, tap the spacebar with one finger, try to replicate your initial beat.\n\nPress 'space' to start.", 
                                   color="white", height=40, wrapWidth=800)                            

end_text = visual.TextStim(win, text="Thank you! The experiment is over.", color="white", height=40)

# Define the pulsating circle
circle = visual.Circle(win, radius=80, fillColor='white', lineColor='white')

# Define fixation cross
fixation = visual.TextStim(win, text="+", color="white", height=150)

# Set up timing parameters
duration = 60  # Duration of each phase in seconds
image_task_duration = 60  # Time allocated for the image task (in seconds)

# Load image file names
image_folder = "./"  # Images are in the same folder as the program
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

# Initialize clock
clock = core.Clock()

# Function to record key presses (tapping) with fixation cross
def record_tapping(clock, duration, task_name):
    tapping_data = []
    end_time = clock.getTime() + duration

    while clock.getTime() < end_time:
        # Draw the fixation cross
        fixation.draw()
        win.flip()

        # Check for key presses
        keys = event.getKeys(timeStamped=clock)
        for key, timestamp in keys:
            if key == 'space':
                tapping_data.append({'event': f'{task_name}_keypress', 'timestamp': timestamp})
            elif key == 'escape':  # Exit on 'escape' key
                win.close()
                core.quit()
    return tapping_data

# Function for synchronized visual and auditory pulsation
def pulsating_circle(clock, metronome, duration, include_metronome=False):
    pulsation_data = []  # Store timestamps of events
    end_time = clock.getTime() + duration
    next_event_time = clock.getTime()  # Unified timing for both sound and circle

    print("Starting pulsating circle with optional metronome...")
    while clock.getTime() < end_time:
        current_time = clock.getTime()

        # Trigger both sound and circle at the same time
        if current_time >= next_event_time:
            # Handle circle visibility for visual tasks
            if task_type in ["Visual Pulsation", "Both"]:
                circle.setOpacity(1.0)  # Circle visible
                pulsation_data.append({'event': 'pulsation', 'timestamp': current_time})

            # Handle metronome sound for auditory tasks
            if include_metronome and task_type in ["Metronome", "Both"]:
                metronome.play()  # Play the metronome sound
                core.wait(beat_interval - offset)  # Offset to synchronise
                metronome.stop()  # Ensure sound is stopped before the next beat

            # Schedule the next event
            next_event_time += beat_interval

        # Visual stimuli logic
        if task_type == "Metronome":
            fixation.draw()  # Show the static fixation cross
        elif task_type in ["Visual Pulsation", "Both"]:
            # Handle circle visibility for visual tasks
            if current_time >= next_event_time - (beat_interval / 2):
                circle.setOpacity(0.0)  # Circle invisible
            else:
                circle.setOpacity(1.0)  # Circle visible
            circle.draw()
        # Refresh the display
        win.flip()

    print("Pulsating circle with metronome complete.")
    return pulsation_data


# Function for Image Description Task
def image_description_task(clock, image_task_duration, image_files):
    description_data = []
    end_time = clock.getTime() + image_task_duration
    image_index = 0  # Start with the first image

    print("Starting Image Description Task...")
    while clock.getTime() < end_time:
        # Load the current image
        current_image = image_files[image_index]
        image_stim = visual.ImageStim(win, image=os.path.join(image_folder, current_image), pos=(0, 0), size=(600, 600))

        # Draw the image
        image_stim.draw()
        win.flip()

        # Check for key presses 
        keys = event.getKeys(keyList=['right', 'escape'], timeStamped=clock)

        # Handle key presses
        for key, timestamp in keys:
            if key == 'right':
                # Record the description event
                description_data.append({
                    'event': 'image_description',
                    'image': current_image,
                    'timestamp': timestamp
                })

                # Move to the next image
                image_index = (image_index + 1) % len(image_files)  # Loop to the start if at the end
            elif key == 'escape':
                win.close()
                core.quit()

    print("Image Description Task complete.")
    return description_data

# Save the current date and time
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Phase 1: Tap to a blank screen with fixation cross
instruction_text.draw()
win.flip()
event.waitKeys(keyList=['space'])  # Wait for participant to press 'space' to start
print("Starting Phase 1: Tapping")
tapping_data = record_tapping(clock, duration, task_name="first_tapping")

# Pause Phase: Instruction for next phase
pause_text.draw()
win.flip()
core.wait(5)  # Wait 5 seconds

# Phase 2: Pulsating Circle or Metronome
print("Starting Phase 2: Pulsating Circle or Metronome")
pulsation_data = pulsating_circle(clock, duration=duration, metronome=metronome, include_metronome=(task_type in ["Metronome", "Both"]))

# Pause Phase 2: Instruction for next phase
pause2_text.draw()
win.flip()
core.wait(5)  # Wait 5 seconds

# Phase 3: Image Description Task
print("Starting Phase 3: Image Description Task")
description_data = image_description_task(clock, image_task_duration, image_files)

# Phase 4: Second tapping task with fixation cross
print("Starting Phase 4: Replicating the Rhythm")
instruction2_text.draw()
win.flip()
event.waitKeys(keyList=['space'])  # Wait for participant to press 'space' to start
second_tapping_data = record_tapping(clock, duration, task_name="second_tapping")

# End Message
end_text.draw()
win.flip()
core.wait(5)  # Show end message for 5 seconds

# Save Data
output_filename = f"participant_{participant_id}_data.csv"
with open(output_filename, mode='w', newline='') as file:
    fieldnames = ['event', 'image', 'timestamp', 'task_type', 'frequency', 'participant_age', 'musical_experience', 'formal_education','early_trained', 'gender', 'l1', 'country', 'datetime']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data in tapping_data + pulsation_data + description_data + second_tapping_data:
        data['task_type'] = task_type #Add type of stimuli used
        data['frequency'] = frequency_choice #Add frequency of pulsation
        data['participant_age'] = participant_age  # Add participant age to each row
        data['musical_experience'] = musical_experience  # Add musical experience to each row
        data['formal_education'] = formal_education #Add wether participant is formally educated in music
        data['early_trained'] = early_trained # Wether participant is early trained or not
        data['gender'] = participant_gender # Add gender
        data['l1'] = participant_language # Add L1 
        data['country'] = participant_country #Add country of Origin
        data['datetime'] = current_datetime  # Add current datetime
        writer.writerow(data)


# Close the window
win.close()
core.quit()
