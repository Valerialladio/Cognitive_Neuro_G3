#import libraries
import psychtoolbox as ptb
from psychopy import prefs, core, visual, event, sound
import glob
import pandas as pd
import os
prefs.hardware['audioLib'] = ['PTB'] #inserting preference here for lowest latency option

# define logfile 
# prepare pandas data frame for recorded data
columns = ['trial_number','response', 'trial_type', 'music_condition', 'stim_condition']
logfile = pd.DataFrame(columns=columns)

# define fixation cross
def fixation(win):
    msg = visual.TextStim(win,"+")
    msg.draw()
    win.flip()
    core.wait(0.5)
visual.TextStim()

# make sure that there is a logfile directory and otherwise make one
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

date = "test"
# define logfile name
logfile_name = "logfiles/logfile_{}.csv".format(date)

#define function for keyboard input
def get_response(img):
    key = event.waitKeys(keyList = ["left", "right", "escape"]) #which keys should be used for response?
    if key[0] == "escape":
        core.quit()
    else:
        response = key[0] 
    return response

# read csv file containing names of stimuli folders
df = pd.read_csv("my_data.csv") 
#contains 5 columns: 
#[trial_type]: 0 or 1, (for action or sentence)
#[music] name of folder containing 8 audio files
#[stim] either a string of word segments separeated by ";" or folder name of 8 images 
#[music_condition] 0 or 1 for congruent or incongruent
#[stim_condition] 0 or 1 for coherent or incoherent

trial_number = 0 #initialise this counting variable

# define window
win = visual.Window(fullscr=True)
#loop through trials
for i in range(3): #80 irl, or 40 if we do break between blocks
    trial_number += 1
    sound_folder_name = df.iloc[i,1] + "/*"
    my_sound_list = glob.glob(sound_folder_name)
    fixation(win)
    if df.iloc[i,0] == 1: #check for language or action
        my_word_list = df.iloc[i,2].split(sep = ";") #list
        
        for j in range(7): #loop through sentence
            
            my_sound = sound.Sound(my_sound_list[j], secs = 0.6)
            text = my_word_list[j]
            
            
            nextFlip = win.getFutureFlipTime(clock='ptb')
            my_sound.play(when=nextFlip)
              
            msg = visual.TextStim(win, text)
            msg.draw()
            win.flip() #implement trigger for this (or only when i==7?)
            core.wait(0.6)
        #do last trial out of loop to do trigger and different core.wait time    
        my_sound = sound.Sound(my_sound_list[7], secs = 1.2) 
        text = my_word_list[7]
        
        
        nextFlip = win.getFutureFlipTime(clock='ptb')
        my_sound.play(when=nextFlip)
        
        msg = visual.TextStim(win, text)
        msg.draw()
        win.flip() #implement trigger for this
        core.wait(1.2)
        
        msg = visual.TextStim(win, "was this sentence semantically coherent") #change this question?
        msg.draw()
        win.flip()
        response = get_response(msg)
        
        
    else: 
        img_folder_name = df.iloc[i,2] + "/*"
        my_img_list= glob.glob(img_folder_name)
        for j in range(7): #loop through pictures
            my_sound = sound.Sound(my_sound_list[j], secs = 0.6) 
            img = my_img_list[j] #do we need to do something special about file path here?
            
            
            nextFlip = win.getFutureFlipTime(clock='ptb')
            my_sound.play(when=nextFlip)
            

            msg = visual.ImageStim(win, img)
            msg.draw()
            win.flip() #implement trigger for this (or only when i==7?)
            core.wait(0.6)
#do last trial out of loop to do trigger and different core.wait time    
        my_sound = sound.Sound(my_sound_list[7], secs = 1.2) 
            
        nextFlip = win.getFutureFlipTime(clock='ptb')
        my_sound.play(when=nextFlip)
            
        img = my_img_list[7]
        msg = visual.ImageStim(win, img)
        msg.draw()
        win.flip() #implement trigger for this 
        core.wait(1.2)
        
        msg = visual.TextStim(win, "was this action semantically coherent") #change this question?
        msg.draw()
        win.flip()
        response = get_response(msg)
        
    logfile = logfile.append({
    'trial_number': trial_number,
    'response': response,
    'trial_type': df.iloc[i,0],
    'music_condition': df.iloc[i,3],
    'stim_condition': df.iloc[i,4]}, ignore_index = True)
    

logfile.to_csv(logfile_name)