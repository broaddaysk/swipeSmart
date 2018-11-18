from tkinter import *
from PIL import ImageTk, Image
import os
from shutil import copy

root = Tk()
lock = 0;

directories = list()

for subfolder in os.listdir('dataset'):
  directories.append(subfolder) 

userdir = 'dataset/' + directories[0]
photodir = userdir + '/' + os.listdir(userdir)[0]

# event => keypress event
#
# When the user presses the left arrow key the current user's image being viewed
# is put in the dislike folder along with the other photos of the user. The next
# user's image is loaded.
def left_key(event):
  global userdir
  if len(directories) is not 0:
    for ui in os.listdir(userdir):
      if ui[0] is not '.':
        temp_photodir = userdir + '/' + ui
        # copies stored in sorted_data/dislike. May need to change to store elsewhere.
        if not os.path.exists('sorted_data/dislike'):
          os.makedirs('sorted_data/dislike')
        copy(temp_photodir, 'sorted_data/dislike')

    directories.pop(0)
    userdir = 'dataset/' + directories[0]
    photodir = userdir + '/' + os.listdir(userdir)[0]
    img = ImageTk.PhotoImage(Image.open(photodir))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.image = img

# event => keypress event
#
# When the user presses the left arrow key the current user's image being viewed
# is put in the dislike folder along with the other photos of the user. The next
# user's image is loaded.
def right_key(event):
  global userdir
  if len(directories) is not 0:
    for ui in os.listdir(userdir):
      if ui[0] is not '.':
        temp_photodir = userdir + '/' + ui
        # copies stored in sorted_data/like. May need to change to store elsewhere.
        if not os.path.exists('sorted_data/like'):
          os.makedirs('sorted_data/like')
        copy(temp_photodir, 'sorted_data/like')

    directories.pop(0)
    userdir = 'dataset/' + directories[0]
    photodir = userdir + '/' + os.listdir(userdir)[0]
    img = ImageTk.PhotoImage(Image.open(photodir))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.image = img

# event => mouse click event
#
# This function refocuses the canvas. Make sure to click on the canvas initially
# to start up the program.
def callback(event):
  canvas.focus_set()
  global lock
  if lock is 0:
    lock = 1
    img = ImageTk.PhotoImage(Image.open(photodir))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.image = img


canvas = Canvas(root, width=320, height=400)
canvas.bind("<Left>", left_key)
canvas.bind("<Right>", right_key)
canvas.bind("<Button-1>", callback)
canvas.pack()

root.mainloop()

# TODO: fix freezing issue that occurs close to the end (can't tell if frozen or finished)

# also add undo function