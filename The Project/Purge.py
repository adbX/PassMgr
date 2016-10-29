import os

def Purge():	
	f = open("test.txt", "wb")
	f.write("*"*os.path.getsize("test.txt"))
	f.close()
	os.unlink("test.txt")