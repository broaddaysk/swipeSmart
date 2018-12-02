from os import listdir
import os
import numpy as np
import cv2
from random import randint

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def rebalance(like_path, dislike_path):
  like_images = listdir(like_path)
  dislike_images = listdir(dislike_path)

  if len(like_images) < len(dislike_images):
    while len(dislike_images) > len(like_images):
      idx = randint(0, len(dislike_images)-1)
      if dislike_images[idx][0] is not '.':
        os.remove(dislike_path + '/' + dislike_images[idx])
        del dislike_images[idx]

  elif len(like_images) > len(dislike_images):
    while len(like_images) > len(dislike_images):
      idx = randint(0, len(like_images)-1)
      if like_images[idx][0] is not '.':
        os.remove(like_path + '/' + like_images[idx])
        del like_images[idx]

# dirname => relative path to the directory that contains the photos
# 
# This function takes a set of images and crops the faces out in the pictures
# as well as grayscale and resizes the cropped images.
def preprocess(dirname):
  for file in listdir(dirname):
    if file[0] is not '.':
      image = cv2.imread(dirname + '/' + file)
      grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(grayscale_image, 1.3, 5)

      if faces is not () and len(faces) is 1:
        cropped_image = grayscale_image[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]
        resized_image = cv2.resize(cropped_image, (256, 256))
        # saves to a folder called processed_photos. May want to change this to save somewhere else.
        
        category = dirname.split("/")[-1]
        if not os.path.exists('sorted_data/processed_' + category):
          os.makedirs('sorted_data/processed_' + category)
        cv2.imwrite('sorted_data/processed_' + category + '/' + file, resized_image)

# like_path => relative path to the directory that contains liked photos
# dislike_path => relative path to the directory that contains disiked photos
#
# This function takes the path to the like and dislike folders and returns a numpy
# representation for the images and corresponding labels.
def get_numpy_repr(like_path, dislike_path):
  images = []
  labels = []
  for img in os.listdir(like_path):
    if img[0] is not '.':
      images.append(cv2.imread(os.path.join(like_path, img)))
      labels.append(1)

  for img in os.listdir(dislike_path):
    if img[0] is not '.':
      images.append(cv2.imread(os.path.join(dislike_path, img)))
      labels.append(0)

  images = np.array(images)
  labels = np.array(labels)

  print("saving {}.npy".format('processed_images'))
  np.save('processed_images', images)

  print("saving {}.npy".format('processed_labels'))
  np.save('processed_labels', labels)

if __name__ == '__main__':
  preprocess('sorted_data/like')
  preprocess('sorted_data/dislike')
  rebalance('sorted_data/processed_like', 'sorted_data/processed_dislike')
  get_numpy_repr('sorted_data/processed_like','sorted_data/processed_dislike')

# need to check relative and absolute sizes of likes/dislikes
# if either category has too few, give warning (what is baseline?)

# log amount of like/dislike images after processing
