from __future__ import unicode_literals
import youtube_dl
import os
import cv2
import threading
import random

def main():
	with open("videolist.txt", "r", encoding="utf-8") as f:
		data = f.read()

	data = data.split("\n")
	for i in data:
		try:
			ydl_opts = {
				'outtmpl': '/videos/%(title)s.%(ext)s',
				'restrictfilenames':True,
				'forcefilename':True,
			}
			# os.chdir('C:/Users/Desktop')
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				# info_dict = ydl.extract_info(i, download=False)
				# name = info_dict['uploader'].replace(" ","_")
				info = ydl.extract_info(i, download=True)
				filepath = ydl.prepare_filename(info)
				print(filepath)
				# extractImages(filepath)

			threading.Thread(target=extractImages, args=[filepath, ]).start()
		except Exception as e:
			print(e)


def extractImages(filepath):
	name = filepath.split("\\")[1]
	name = name.split(".")[0]
	pathOut="images/" + name + "/"
	print(pathOut)
	while True:
		try:
			os.mkdir(pathOut)
			break
		except Exception as e:
			pathOut="images/" + name + str(random.randint(0, 1000000)) + "/"
			print(e)

	count = 0
	vidcap = cv2.VideoCapture(filepath)
	success,image = vidcap.read()
	success = True

	while success:
		if count%3==0:
			vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
			success,image = vidcap.read()
			# print ('Read a new frame: ', success)
			cv2.imwrite( pathOut + "frame%d.jpg" % count, image)     # save frame as JPEG file
		count = count + 1

main()
