from psychopy import visual, core, event, gui
import random
import csv
import re  # Import regex module for number stripping


# Participant Info Dialog
participant_dialog = gui.Dlg(title="Participant Info")
participant_dialog.addField("Participant ID:")
participant_dialog.show()

if participant_dialog.OK:
    participant_id = participant_dialog.data[0]
else:
    core.quit()
    
# Define fullscreen window
win = visual.Window(color=[-1, -1, -1], units="pix", fullscr=True)

# Instruction Dialog
consent_text = visual.TextStim(win, text="You will be asked to evaluate the semantic congruency of some sentences.\n\nPress the left arrow for coherent letters, and the right one for non-coherent. Press the up arrow if the sentence was too fast.\n\n Press spacebar to start or exit to exit the experiment",
                               color="white", height=40, wrapWidth=800)
consent_text.draw()
win.flip()

# Wait for participant to either consent or exit
keys = event.waitKeys(keyList=['space', 'escape'])    

# Load sentences from a text file, removing initial numbers
with open("sentences.txt", "r", encoding="utf-8") as file:
    original_sentences = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in file.readlines()]  # Remove numbers

# Create a shuffled copy for randomized presentation
sentences = original_sentences.copy()
random.shuffle(sentences)

# Create a PsychoPy window
win = visual.Window(fullscr=True, color="black")

# Create a text stimulus
text_stim = visual.TextStim(win, text="", color="white", height=0.08, wrapWidth=1.5)

# Main
# Store results
results = []

for sentence in sentences:
    # Get sentence index from original list (1-based indexing)
    sentence_id = original_sentences.index(sentence) + 1

    # Display each sentence segment for 600 ms
    sentence_segments = sentence.split(" - ")  # Splitting sentence into segments
    for i, segment in enumerate(sentence_segments):
        text_stim.text = segment  # Set text
        text_stim.draw()          # Draw text on screen
        win.flip()                # Show text
        core.wait(0.6)            # Wait 600 ms

        # Record the time after the last segment is shown
        if i == len(sentence_segments) - 1:  
            last_segment_time = core.getTime()  

    # Present rating screen
    text_stim.text = "Rate the sentence:\n\nPress 'left arrow' = Coherent\nPress 'right arrow' = Non-Coherent\nPress 'up arrow' = Too fast"
    text_stim.draw()
    win.flip()

    # Wait for valid response and record reaction time
    response = None
    while response not in ["left", "right", "up", "escape"]:
        response_time = core.getTime()  # Get current time
        response = event.waitKeys(keyList=["left", "right", "up", "escape"])[0]

    # Calculate reaction time (RT)
    rt = response_time - last_segment_time  

    # Allow exit if needed
    if response == "escape":
        break

    # Store result with sentence ID and RT instead of full text
    results.append({"sentence_id": sentence_id, "response": response, "reaction_time": round(rt, 3)})

# Save Data
# Write responses to a CSV file
filename = f"participant_{participant_id}_data.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["sentence_id", "response", "reaction_time"])
    writer.writeheader()
    writer.writerows(results)

win.close()
core.quit()

