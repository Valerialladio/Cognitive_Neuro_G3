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
    for segment in sentence.split(" - "): 
        text_stim.text = segment  # Set text
        text_stim.draw()          # Draw text on screen
        win.flip()                # Show text
        core.wait(0.6)            # Wait 600 ms

    # Present rating screen
    text_stim.text = "Rate the sentence:\n\nPress 'N' = Coherent\nPress 'M' = Non-Coherent\nPress 'L' = Too fast"
    text_stim.draw()
    win.flip()

    # Wait for valid response
    response = None
    while response not in ["n", "m", "l", "escape"]:
        response = event.waitKeys(keyList=["n", "m", "l", "escape"])[0]

    # Allow exit if needed
    if response == "escape":
        break

    # Store result with sentence ID instead of full text
    results.append({"sentence_id": sentence_id, "response": response})

#Save Data
# Write responses to a CSV file
filename = f"participant_{participant_id}_data.csv"
with open(filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["sentence_id", "response"])
    writer.writeheader()
    writer.writerows(results)


win.close()
core.quit()
