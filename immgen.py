from PIL import Image, ImageOps, ImageDraw, ImageFont,ImageChops
import numpy as np
from io import StringIO
import csv

bordo = Image.open('/home/nic/progetti/orto/bordo.png')
logo = Image.open('/home/nic/progetti/orto/logorto.jpg')
bkg = Image.open('/home/nic/progetti/orto/bkg2.png')

f = open('/home/nic/progetti/orto/Trees2.csv', "r")
lines = f.read().split("\n") # "\r\n" if needed

font = ImageFont.truetype("/home/nic/.local/share/fonts/Unknown Vendor/TrueType/Harding Text Web/Harding_Text_Web_Regular.ttf", 90)
bold = ImageFont.truetype("/home/nic/.local/share/fonts/Commercial Type/TrueType/Harding Text Web/Harding_Text_Web_Bold.ttf", 100)
italic = ImageFont.truetype("/home/nic/.local/share/fonts/Unknown Vendor/TrueType/Harding Text Web/Harding_Text_Web_Italic.ttf", 60)


a=('ACER MONSPESSULANUM,Acero Minore,Fam. Aceraceae', 'ACER PSEUDOPLATANUS,Acero Di Monte,Fam. Aceraceae', 'METASEQUOIA GLYPTOSTROBOIDES,Metasequoia,Fam. Cupressaceae' )
i=0
b=(19,23,90)
for line in a:
    print("Generatin")
    #if line != "": # add other needed checks to skip titles
    nomepianta = line.split(",")
    nomone = nomepianta[0].split(" ")
    print(nomepianta[1])

    im = Image.new(mode = "RGB", size = (1772, 1181), color = (255, 255, 255))
    qr = Image.open('/home/nic/progetti/orto/imm/{:04d}.png'.format(b[i]))
    #qr = Image.open('/home/nic/progetti/orto/imm/0000.png')
    logo = logo.resize((550, 550), Image.ANTIALIAS)
    qr = qr.resize((650, 650), Image.ANTIALIAS)
    im.paste(qr,  (1100, 550))
    im.paste(logo,  (1170, 50))
    im = ImageChops.multiply(im, bkg)

    d = ImageDraw.Draw(im)
    #ocio metaseq
    d.text((80, 250),nomone[0],(0,0,0),font=bold)
    d.text((80, 400),nomone[1],(0,0,0),font=bold)
    d.text((80, 650),nomepianta[1],(0,0,0),font=font)
    d.text((80, 850),nomepianta[2],(0,0,0),font=italic)

    #d.text((80, 850), '{:d}'.format(i),(100,60,50),font=italic)
    outfile='/home/nic/progetti/orto/final1/{:04d}.png'.format(b[i])
    im.save(outfile, "PNG", quality=100)
    i=i+1
    im.close()

