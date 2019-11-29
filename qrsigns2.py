###################################################
# This is a script to create multiple QR labels
# with some text and a logo image from a csv file
#
# I used this script to generate ~200 garden signs
# in .png format for the Botanical Garden at
# San Giovanni in Persiceto (BO)
#
# author: Nicola Borghi
# e-mail: nicoborghi [at] outlook.com
#
###################################################

# Import libraries
import os
import sys 
import qrcode

from pandas import read_csv 
from PIL import Image, ImageFont, ImageChops, ImageDraw


os.chdir('/home/nic/progetti/orto/')
# Directory definition
dir_home = os.getcwd()
dir_imm = dir_home+'/signs/'
dir_qr = dir_home+'/qr/'

# Filename definition
filecsv='input.csv'

# Creation of the directories
if not os.path.exists(dir_imm):
	os.mkdir(dir_imm)
	print("Directory " , dir_imm ,  " created ")
else:
	print("Directory " , dir_imm ,  " already existing")
if not os.path.exists(dir_qr):
	os.mkdir(dir_qr)
	print("Directory " , dir_qr ,  " created ")
else:
	print("Directory " , dir_qr ,  " already existing")

# Check for the existence of the input '.csv' file
if not os.path.isfile(filecsv):
    sys.exit("\nError: File {:s} not found in the current working directory. Have a nice day!\n".format(filecsv))


df = read_csv(filecsv) 
#print (df['URL'])    #sanity check


####################
#                  #
#  Graphic Design  #
#                  #
####################

# Image Components
logo = Image.open('logo.jpg')
wwf = Image.open('wwf.png')
mct = Image.open('mct.png')
logo = logo.resize((375, 350), Image.ANTIALIAS)
mct = mct.resize((467, 350), Image.ANTIALIAS)
wwf = wwf.resize((236, 350), Image.ANTIALIAS)
bkg = Image.open('background.png')


# Fonts
fontreg = ImageFont.truetype("/home/nic/.local/share/fonts/Unknown Vendor/TrueType/Harding Text Web/Harding_Text_Web_Regular.ttf", 95)
fontbold = ImageFont.truetype("/home/nic/.local/share/fonts/Commercial Type/TrueType/Harding Text Web/Harding_Text_Web_Bold.ttf", 100)
fontit = ImageFont.truetype("/home/nic/.local/share/fonts/Unknown Vendor/TrueType/Harding Text Web/Harding_Text_Web_Italic.ttf", 80)



for i in range(len(df)):
    #QR Code generation
    print("Generating: {:s}".format(df['URL'][i]))
    qr = qrcode.make(df['URL'][i])
    qrfile=dir_qr+"{:04d}.png".format(i)
    qr.save(qrfile)

    # Sign design: qr, logo and background
    sizeimm=(1772, 1181)
    imm = Image.new(mode = "RGB", size = sizeimm, color = (255, 255, 255))
    qr = qr.resize((570, 570), Image.ANTIALIAS)
    imm.paste(qr,  (20, 20))
    imm.paste(mct,  (550, 100))
    imm.paste(logo,  (970, 90))
    imm.paste(wwf,  (1410, 90))
    imm = ImageChops.multiply(imm, bkg) # Multiplication of the background

    txt = ImageDraw.Draw(imm)
    
    W, H = (443,750)
    msg=df['Text_1'][i]
    w, h = txt.textsize(msg)
    txt.text((90,620), msg,(0,0,0),font=fontbold)
    
    W, H = (443,950)
    msg=df['Text_2'][i]
    w, h = txt.textsize(msg)
    txt.text((90,790), msg,(0,0,0),font=fontreg)


    msg=df['Text_3'][i]
    txt.text((950,1020),msg,(0,0,0),font=fontit)


    # Save Images
    immfile=dir_imm+"{:04d}.png".format(i)
    imm.save(immfile, "PNG", quality=100)
    imm.close()