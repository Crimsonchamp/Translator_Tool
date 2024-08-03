import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from idlelib.tooltip import Hovertip
import pyautogui
from PIL import Image,ImageOps
from pytesseract import pytesseract
from transformers import MarianMTModel, MarianTokenizer
import os


#tkinter used for the display
#pyautogui used to screenshot window location
#PIL Image used to open image into image object
#pytesseract used to extract string from image
#Using MarianMTModel and MarianTokenizer for translation

#Establish script location and screenshot location directory
script_dir = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(script_dir, 'screenshots')
os.makedirs(screenshots_dir, exist_ok=True)


window_size= "800x500"

#Root is being used as Entry Window
root = tk.Tk()
root.geometry(window_size)
root.title('Translator')

#Keeps track of enumerated windows
top_bucket = []

#Language selection for MT
def language_selector(lang):
    global language,language_model
    language=lang
    if language == 'jpn':
        language_model = 'Helsinki-NLP/opus-mt-ja-en'
    if language == 'chi_sim' or 'chi_tra': 
        language_model = 'Helsinki-NLP/opus-mt-zh-en'
    lang_pick_label.config(text=f'Chosen:{language}')
    
language = 'jpn'
language_model = 'Helsinki-NLP/opus-mt-ja-en'


#Initializes the Machine translator with a language
model = MarianMTModel.from_pretrained(language_model)
tokenizer= MarianTokenizer.from_pretrained(language_model)

def createWindow():
    #Windows generated from root will be named Top, as they will remain on top
    #wm_attributes are set as -config,set attribute
    #We are setting backgroudn of window to same transparency as background of text labels.
    top= tk.Toplevel(root)
    top.geometry(window_size)
    top.grid
    top.wm_attributes("-transparentcolor",'#ab23ff','-topmost',"true")
    top.config(bg = '#ab23ff')

    #This is where raw text will be displayed
    image_text = 'Empty'
    raw_label = Label(top, text=f"{image_text}", font= ('Helvetica 14'), bg= 'black',fg= 'yellow',wraplength=1000)
    

    #This is where translated text will be displayed
    t_label = Label(top, text=f"{image_text}", font= ('Helvetica 14'), bg= 'black',fg= 'green',wraplength=1000)
    
    

    #Just to know I can do this, if you want to add a text field
    #entry = Entry(top)
    #entry.pack()

    #For testing, get's coodrinates of top window, and size
    #def get_xy():
        #print(top.winfo_x(),top.winfo_y(), top.winfo_width(), top.winfo_height())
    #os_but = tk.Button(top,text="Position", command=get_xy)
    #pos_but.grid(column=0,row=0)

    #Uses Top Window's coordinates to take a screenshot beneath itself.
    def screen_shot():
        region = (top.winfo_x()+120,top.winfo_y()+35,top.winfo_width()-100,top.winfo_height())
        pyautogui.screenshot(rf'{screenshots_dir}\{top.title()}.png', region=region)


    #Uses screenshot taken to extract text.
    def img_to_txt():
        path_to_tesseract= r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        image_path=rf'{screenshots_dir}\{top.title()}.png'
        img = Image.open(image_path)
        img = ImageOps.invert(img)
        img.convert('L')
        pytesseract.tesseract_cmd = path_to_tesseract
        raw_text = (pytesseract.image_to_string
                    (img,lang=language,config=f'{psm} -c tessedit_char_blacklist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))
        raw_label.config(text=raw_text) 
        print(raw_text)
        t_text = translate_text(raw_text)
        print(t_text)
        t_label.config(text=t_text)

        #Uses the MarianMTModel to generate translated text from raw_text
    def translate_text(raw_text):
        trans_text = model.generate(**tokenizer(raw_text,return_tensors="pt",padding=True))
        return tokenizer.decode(trans_text[0],skip_special_tokens=True)
    

        
    #Button to clear the text for clear screenshot
    def clear_text():
        raw_label.config(text='')
        t_label.config(text='')
    
    def psm_configure(psm_input='--psm 6'):
        global psm
        psm = psm_input
        psm_label.config(text=f'{psm}')

    #Button linking to functions
    scree_but = tk.Button(top,text="Screenshot!",width=15, command=screen_shot)
    img_to_txt_but = tk.Button(top,text="What did I see?",width=15, command=img_to_txt)
    clear_but = tk.Button(top,text="Clear text",width=15, command=clear_text)

    #PSM buttons
    psm3_but = tk.Button(top,text="3-Default",command=lambda:psm_configure('--psm 3'))
    psm4_but = tk.Button(top,text="4-Receipt-like",command=lambda:psm_configure('--psm 4'))
    psm5_but = tk.Button(top,text="5-4 but rotated",command=lambda:psm_configure('--psm 5'))
    psm6_but = tk.Button(top,text="6-Uniform text",command=lambda:psm_configure('--psm 6'))
    psm7_but = tk.Button(top,text="7-Uniform line",command=lambda:psm_configure('--psm 7'))
    psm8_but = tk.Button(top,text="8-Word",command=lambda:psm_configure('--psm 8'))
    psm10_but = tk.Button(top,text="10-Character",command=lambda:psm_configure('--psm 10'))
    psm11_but = tk.Button(top,text="11-Sparse Text",command=lambda:psm_configure('--psm 11'))
    psm13_but = tk.Button(top,text="13-Raw Line",command=lambda:psm_configure('--psm 13'))


    #Setting the sidebar.
    sidebar_frame = tk.Frame(top)
    sidebar_frame.grid(row=0,column=0,sticky="nsew")

    #Setting some sidebar labels
    border_label= Label(top,bg="light grey",relief="sunken",width=15,height=200)
    psm_label= Label(top,bg="black",fg="white",text=f'PSM')
    
    #Label and button positions
    scree_but.grid(column=0,row=1,sticky="nsew")
    img_to_txt_but.grid(column=0,row=2,sticky="nsew")
    clear_but.grid(column=0,row=3,sticky="nsew")
    psm_label.grid(column=0,row=4,sticky="nsew")
    psm3_but.grid(column=0,row=5,sticky="nsew")
    psm4_but.grid(column=0,row=6,sticky="nsew")
    psm5_but.grid(column=0,row=7,sticky="nsew")
    psm6_but.grid(column=0,row=8,sticky="nsew")
    psm7_but.grid(column=0,row=9,sticky="nsew")
    psm8_but.grid(column=0,row=10,sticky="nsew")
    psm10_but.grid(column=0,row=11,sticky="nsew")
    psm11_but.grid(column=0,row=12,sticky="nsew")
    psm13_but.grid(column=0,row=13,sticky="nsew")
    border_label.grid(column=0,row=14,rowspan=200)
    raw_label.grid(column=2,row=1,columnspan=10, rowspan=5)
    t_label.grid(column=2,row=6,columnspan=10, rowspan=10)

    #tool tips, needed to force it to top level due to windows already being on top level.
    class CustomHovertip(Hovertip):
        def showtip(self):
            super().showtip()
            if self.tipwindow:
                self.tipwindow.lift()
                self.tipwindow.attributes('-topmost', True)
        

    CustomHovertip(psm3_but, "The Default setting, without orientation.")
    CustomHovertip(psm4_but, "Scans text like a Receipt or Menu.")
    CustomHovertip(psm5_but, "Scans text vertically, but like a Receipt or Menu, like 4 but rotated.")
    CustomHovertip(psm6_but, "Best at scanning book pages, large blocks of uniform text.")
    CustomHovertip(psm7_but, "Best at scanning a single uniform line, like a licence plate.")
    CustomHovertip(psm8_but, "Best at scanning a single word.")
    CustomHovertip(psm10_but, "Best at scanning a single character.")
    CustomHovertip(psm11_but, "When text is sparse and spread out, without order.")
    CustomHovertip(psm13_but, "If text is an unusual format or font, you can try using this. Like a Wildcard.")
    

    #Enumerates the extra windows created, which controls the name of the screenshots as well
    if len(top_bucket) == 0:
        top.title(0)
    else:
        top.title(len(top_bucket))
    top_bucket.append(top)


instruction="Instructions:\nChoose your desired language translation and hit new window.\
In the new window, you will see new options:\n\
Screenshot!:Will create a screenshot of the clear field of the window, named as the window's title.\n\
What did I see?: Will return the raw text in yellow and translated text in green\n\
Clear text: Will clear the current raw and translated text. Do this prior to each screenshot.\n\n\
Screenshot! - > What did I see? - > Clear text\n\n\
Troubleshooting: The scraping isn't always the most accurate, you can jostle the window a bit\n\
for a different result. It works best on images of the 300dpi range. Try using different PSMs"
greeting=   "Hello! I'm Crimsonchamp(or Jules).\n\
This was my first independent project, inspired by an old machine translation program\
 I used some many years ago. If running this as a script, you will need to install the dependencies.\n\
It uses: \n\
            tkinter for the visual render\n\
            pyautogui for screenshotting\n\
            Pillow for image manipulation\n\
            pytesseract for text-scraping\n\
            Marian model for translation"

#When 'New Window' is pressed, creates top type window.
lang_pick_label = Label(root, text=f"Chosen:{language}",width=25, font= ('Helvetica 14'),wraplength=1000)
instruction_label = Label(root, text=f"{instruction}",font=('Helvetica 12'),bg="light grey",relief="sunken",justify=LEFT,width=82,wraplength=750)
greetings_label = Label(root,text=f"{greeting}",font=('Helvectica 12'),bg="light grey",relief="sunken",justify=LEFT,width=82,wraplength=750,anchor='s')
jpn_button = Button(root, text= "Japanese to English",width=25 ,command=lambda: language_selector('jpn'))
chi_sim_button = Button(root, text= "Simplified Chinese to English",width=25,command=lambda: language_selector('chi_sim'))
chi_tra_button = Button(root, text= "Traditional Chinese to English",width=25,command=lambda: language_selector('chi_tra'))
window_button = Button(root, text = "New Window", command= createWindow)
lang_pick_label.pack()
jpn_button.pack()
chi_sim_button.pack()
chi_tra_button.pack()
window_button.pack()
instruction_label.pack()
greetings_label.pack()

root.mainloop()