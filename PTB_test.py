#import libraries
import psychtoolbox as ptb
from psychopy import prefs, core, visual, sound
prefs.hardware['audioLib'] = ['PTB'] #inserting preference here for lowest latency option

# define sound files
c_sound = sound.Sound('C_test.wav', secs = 0.6)
f_sound = sound.Sound('F_test.wav', secs = 0.6)
g_sound = sound.Sound('G_test.wav', secs = 0.6)

# define the window and words. 
win = visual.Window(fullscr=True)
msg1 = visual.TextStim(win, "word1")
msg2 = visual.TextStim(win, "word2")
msg3 = visual.TextStim(win, "word3")
msg4 = visual.TextStim(win, "word4")

#prep the next sound
nextFlip = win.getFutureFlipTime(clock='ptb')
c_sound.play(when=nextFlip)

#present stim
msg1.draw()
win.flip()
core.wait(0.6) #wait 600ms. while sound plays


# repeat etc... this should be a loop but this is a simple test
nextFlip = win.getFutureFlipTime(clock='ptb')
f_sound.play(when=nextFlip)

msg2.draw()
win.flip()
core.wait(0.6)

nextFlip = win.getFutureFlipTime(clock='ptb')
g_sound.play(when=nextFlip)

msg3.draw()
win.flip()
core.wait(0.6)

nextFlip = win.getFutureFlipTime(clock='ptb')
c_sound.play(when=nextFlip)

msg4.draw()
win.flip()
core.wait(1.2)