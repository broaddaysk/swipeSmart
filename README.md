pipeline is:

1) scraper.py
	a) INPUT: facebook login info in login.json
	b) scrapes tinder for nearby user photos
	c) OUTPUT: dataset folder with user_id subfolders containing their respective photos

2) label.py
	a) INPUT: dataset folder
	b) manually sort dataset into like/dislike using tinderesque GUI (left arrow key=dislike, right arrow key=like)
	c) OUTPUT: sorted_data folder with like and dislike subfolders containing photos

3) preprocessing.py
	a) INPUT: sorted_data folder
	b) convert all photos to greyscale and resize, then convert images and labels into npy
	c) OUTPUT: processed_like/processed_dislike subfolders in sorted_data, processed_images.npy, processed_labels.npy

4) train.py
	a) INPUT: processed_images.npy, processed_labels.npy
	b) train model
	c) OUTPUT: model.h5

5) bot.py
	a) INPUT: facebook login info in login.json, model.h5
	b) automatically swipes based on model preferences
	c) OUTPUT: matches.csv to store past session matches

TODO: combine into makefile, also use online learning instead

also rm -rf previously made directories
