import pynder
import tensorflow as tf 
import numpy as np 
import robobrowser
import re
import os
import sys
import json
import csv
import cv2
from time import sleep
from random import randint
from skimage.io import imread, imshow, show
#from skimage import io
from skimage.transform import resize


MOBILE_USER_AGENT = r"Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://m.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

def get_access_token(email, password):
	s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
	s.open(FB_AUTH)
	f = s.get_form()
	f["pass"] = password
	f["email"] = email
	s.submit_form(f)
	f = s.get_form()
	if f.submit_fields.get('__CONFIRM__'):
		s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
	else:
		raise Exception("Couldn't find the continue button. Maybe you supplied the wrong login credentials? Or maybe Facebook is asking a security question?")
	access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
	return access_token

def get_login_info():
	if os.path.exists('login.json'):
		with open('login.json') as login_file:
			info = json.load(login_file)
			if "email" in info and "password" in info:
				return (info["email"], info["password"])
			else:
				print("invalid login.json")
				sys.exit(0)
	else:
		print("missing login.json")
		sys.exit(0)

def extract_faces(img):
	img_size = 100
	res_arr = []

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

	grayscale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(grayscale_image, 1.3, 5)

	if faces is not () and len(faces) is 1:
		cropped_image = grayscale_image[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]
		resized_image = cv2.resize(cropped_image, (img_size, img_size))
		res_arr.append(resized_image)
		return res_arr
	else:
		return []

def predict(user, model):
	photos = user.get_photos()

	for photo in photos:

		image = imread(photo)

		#imshow(image)
		#show()
		
		face = np.array(extract_faces(image))

		if len(face) != 0:
			result = model.predict(face)
			if result[0][1] > 0.4:
				return 'like'
			else:
				return 'dislike'
		else:
			print('trying next photo')

def swipe(session, model):
	likes = 0
	dislikes = 0

	while session.likes_remaining > 0:
		users = session.nearby_users()
		try:
			for user in users:
				result = predict(user, model)
				if result == 'like':
					print('liked ' + user.name)
					#user.like()
					likes += 1
					sleep(randint(3,15))
				else:
					print('disliked ' + user.name)
					#user.dislike()
					dislikes += 1
					sleep(randint(3,15))
		except:
			print("error in prediction")


def message_matches(session):
	old_matches = set()
	if os.path.exists('matches.csv'):
		with open('matches.csv', newline='') as read_matches:
			reader = csv.reader(read_matches)
			for row in reader:
				old_matches.add(row[0])

	new_matches = []
	for match in session.matches():
		if match.user.id not in old_matches:
			print('message')
			#match.message('hey cutie')
			new_matches.append(match.user.id)

	with open('matches.csv', 'w', newline='') as write_matches:
		writer = csv.writer(write_matches)
		for user_id in new_matches:
			writer.writerow([user_id])

if __name__ == '__main__':
	print("bot initialized")

	email, password = get_login_info()
	fb_token = get_access_token(email, password) 
	session = pynder.Session(fb_token)
	print("successful login")

	model = tf.keras.models.load_model('model.h5')
	swipe(session, model)
	message_matches(session)