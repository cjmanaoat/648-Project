from PIL import Image
import re
import subprocess

all_items = subprocess.Popen('ls', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
img_list, _ = all_items.communicate()
results = re.findall(rb'\d+.jpg', img_list)
#print(results)
sizes = [(120,120), (720,720)]
for image in results:
    #print(image.decode('utf-8'))
    image = image.decode('utf-8')
    for size in sizes:
        im = Image.open(image)
        im.thumbnail(size)
        #import pdb; pdb.set_trace()
        first, second = size
        #print("thumbnail_%s_res_%d.jpg" % (image[:-4], first))
        im.save("thumbnail_%s_res_%d.jpg" % (image[:-4], first))
