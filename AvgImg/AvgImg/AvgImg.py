import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import tensorflow
from PIL import Image

dir = r'C:\Users\drewm\Downloads\Dogs\\'
data = []

for img in os.listdir(dir):
    if img.endswith('.png'):
        img2 = img.replace('.png', '.jpg')
        os.rename(dir + "\\" + img, dir + "\\" + img2)
count = 0
for img in os.listdir(dir):
    pic = plt.imread(dir + img)

    if pic.shape == (1080, 1920, 3):
        data.append(pic)

    if not (count % 20):
        print(str(count / 1))
    count += 1
    if count == 75:
        break
meanImg = numpy.mean(data, axis = 0)
print(meanImg.shape)
plt.imshow(meanImg.astype('uint8'))
plt.show()

    

    

