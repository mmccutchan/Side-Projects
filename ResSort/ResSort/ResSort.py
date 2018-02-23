from PIL import Image
import os

root = r"C:\Users\drewm\Downloads"
outputDir = input("What should the folder output name be? ")
if outputDir is None:
    os.mkdir(root + "\\" + outputDir)
for file in os.listdir(root):
    try:
        img = Image.open(root + "\\" + file)
        w, h = img.size
        img.close()
        dirName = root + "\\" + outputDir + "\\" + str(w) + "x" + str(h)

        if not (os.path.exists(dirName)):
            os.mkdir(dirName)

        os.rename(root + "\\" + file,  dirName + "\\" + file)
        
    except Exception as e:
        print(str(e))