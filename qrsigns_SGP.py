###################################################
# This is a script to create multiple images with
# QR code, some text, and logos from a .csv file
#
# author: Nicola Borghi
# e-mail: nicoborghi [at] outlook.com
###################################################

# Import libraries
import os
import sys 
import qrcode

from pandas import read_csv 
from PIL import Image, ImageFont, ImageChops, ImageDraw

# Directory definition
dir_home = os.getcwd()
dir_out  = dir_home+'/signs/'
dir_qr   = None

# Fonts definition
fontreg  = ImageFont.truetype("fonts/HardingText-Regular-Web.ttf", 95)
fontbold = ImageFont.truetype("fonts/HardingText-Bold-Web.ttf", 100)
fontit   = ImageFont.truetype("fonts/HardingText-RegularItalic-Web.ttf", 80)

# Input file definition
filecsv='data/orto_botanico_san_giovanni_persiceto.csv'


# Creation of the directories
if not os.path.exists(dir_out):
	os.mkdir(dir_out)
	print("Directory " , dir_out ,  " created ")
else:
	print("Directory " , dir_out ,  " already existing")
	
if dir_qr is not None:
    if not os.path.exists(dir_qr):
        os.mkdir(dir_qr)
        print("Directory " , dir_qr ,  " created ")
    else:
        print("Directory " , dir_qr ,  " already existing")

# Check for the existence of the input '.csv' file
if not os.path.isfile(filecsv):
    sys.exit("\nError: File {:s} not found in the current working directory. Have a nice day!\n".format(filecsv))

df = read_csv(filecsv) 


####################
#                  #
#  Graphic Design  #
#                  #
####################

# Image Components
logo = Image.open('images/logo.jpg')
wwf = Image.open('images/wwf.png')
mct = Image.open('images/mct.png')
bkg = Image.open('images/background.png')

logo = logo.resize((375, 350), Image.Resampling.LANCZOS)
mct = mct.resize((467, 350), Image.Resampling.LANCZOS)
wwf = wwf.resize((236, 350), Image.Resampling.LANCZOS)


for i in range(len(df)):
    #QR Code generation
    print("Generating: {:s}".format(df['URL'][i]))
    qr = qrcode.make(df['URL'][i])
    
    if dir_qr is not None:
        qr.save(dir_qr+"{:04d}.png".format(i))

    # Sign design: qr, logo and background
    sizeimm=(1772, 1181)
    imm = Image.new(mode = "RGB", size = sizeimm, color = (255, 255, 255))
    qr = qr.resize((570, 570), Image.Resampling.LANCZOS)
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
    immfile=dir_out+"{:04d}.png".format(i)
    imm.save(immfile, "PNG", quality=100)
    imm.close()