from tkinter.constants import HORIZONTAL
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pytesseract
import cv2
import PyPDF2
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
import time
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Code Required for ibm_text_to_speech and other requirements
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/332a60c0-d4b0-439b-9e6b-c81245000537"
key = "7eKuHjgh_Hj5cEmwpjFvTaax9n94KOFCKdMID0g4-0lK"
auth = IAMAuthenticator(key)
tts = TextToSpeechV1(authenticator=auth)
tts.set_service_url(url)

# Base path for storing the audio file
base_path = r'E:\python programs\Testing IBM Text-To-Speech'

# Setting up the GUI using Tkinter
root = tk.Tk()
root.title("Audio Book Creater")
root.geometry('720x540')
bg = tk.PhotoImage(file=resource_path('background_img.png'))
canvas = tk.Canvas(root,width=480,height=480)
canvas.pack(fill='both',expand=True)
canvas.create_image(125, 0, image=bg,anchor='nw')


# Function That converts given text to mp3 file
def text_to_mp3_convert(text_file):
    audio_file_path = fd.asksaveasfilename(defaultextension='.mp3',filetypes=[('mp3 files','.mp3')])
    with open(audio_file_path, 'wb') as audio_file:
        res = tts.synthesize(text_file, accept='audio/mp3',voice='en-US_AllisonV3Voice').get_result()
        audio_file.write(res.content)
    

# Function for reading text from image and storing it as an mp3 file
def read_from_image(img_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = ''
    config_ = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=config_)
    text = ' '.join([i.replace('\n','') for i in text.split()])
    text_to_mp3_convert(text)
    

# Function for reading text from a txt file and saving it as an mp3 file
def read_from_txt(file_path):
    with open(file_path, 'r') as f:
        text = f.readlines()
        text = ''.join([i.replace('\n', '') for i in text])
    text_to_mp3_convert(text)


# Function to read data from pdf file and save it as an mp3 file
def read_from_pdf(file_path):
    pdf = open(file_path,'rb')
    pdf_read = PyPDF2.PdfFileReader(pdf)
    length = pdf_read.numPages
    text = ''
    for i in range(length):
        data=pdf_read.getPage(i)
        text+= data.extractText()
    text_to_mp3_convert(text)

# Function to open Files to convert
def open_files():
    global file_path
    file_types=(('text files','*.txt'),('pdf files','*.pdf'),('image files','*.png'))
    try:
        file_path = fd.askopenfilename(filetypes=file_types)
    except AttributeError:
        canvas.create_text(230, 350, text='Please Select a file to convert', anchor='nw', fill='#FF0000',
                           font=('Arial', 14, 'bold'),tags='error')
        canvas.update_idletasks()
        time.sleep(1)
        canvas.delete('error')


# Function that actually converts the loaded file to MP3
def convert():
    global file_path
    if file_path[-3:] == 'txt':
        read_from_txt(file_path)
    elif file_path[-3:] == 'pdf':
        read_from_pdf(file_path)
    else:
        read_from_image(file_path)
    time.sleep(0.5)

    # This Part of the code is to show the conversion progress bar
    prog_bar_canvas = canvas.create_window(315, 300, anchor='nw', window=prog_bar,tags='progbar')
    percent_label_canvas = canvas.create_window(315, 330, anchor='nw', window=percent_label,tags='percent')
    for i in range(100):
        time.sleep(0.05)
        prog_bar['value']+=1
        percent.set(str(prog_bar['val'])+'%'+' Converted')
        root.update_idletasks()
    time.sleep(0.5)
    prog_bar['value']=0
    canvas.delete('progbar')
    canvas.delete('percent')


# Currently added a sample text file path but can choose using the open button
file_path = ''

# Open button to open a certain file
open_button=ttk.Button(root,text='Open a File',command=open_files)

# Convert Button to perform the conversion 
convert_button = ttk.Button(root, text='Make Audio Book', command=convert)

# Progress Bar
prog_bar = ttk.Progressbar(root)

# Conversion Percentage and text
percent = StringVar()
percent_label = ttk.Label(root,textvariable=percent,background='#166cac')

# Creating Canvas for buttons and progress bar
button1 = canvas.create_window(325, 200, anchor='nw', window=open_button)
button2 = canvas.create_window(312, 250, anchor='nw', window=convert_button)


root.mainloop()
