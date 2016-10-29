import os

def txt2mp4():
	x = list(os.path.splitext("test.txt"))
	x[1] = ".mp4"
	y = "".join(x)
	print y
	os.rename("test.txt", y)

def mp42txt():
	x = list(os.path.splitext("test.mp4"))
	x[1] = ".txt"
	y = "".join(x)
	print y
	os.rename("test.mp4", y)

