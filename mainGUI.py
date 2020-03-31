import webbrowser
import os
import tkinter as tk
import functions
import tkinter.font as font
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from os import path



#start the GUI
window = Tk()
#load title
window.title("PDF Miner by William Lima")
#set the dimensions
window.geometry('400x300')
# Gets the requested values of the height and widht.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))
#Font
myFont = font.Font(family='Helvetica', size=14, weight='bold')

galleryprices = ["15.99", "16.99", "17.99", "18.99", "19.99", "20.99", "21.99", "22.99", "23.99", "24.99",
                 "25.99", "26.99", "27.99", "28.99", "29.99", "30.99", "31.99",
                 "32.99", "33.99", "34.99", "35.00", "36.99", "37.99", "38.00"]
dailyprices = ["8.00", "9.00", "10.00", "11.00", "12.00", "13.00", "14.00", "15.00", "16.00", "17.00", "18.00",
               "19.00", "20.00", "21.00", "22.00", "23.00", "24.00", "25.00", "26.00", "27.00", "28.00"]
sweetprices = ["2.99", "3.99", "4.99", "5.99", "6.49", "7.49", "8.49", "4.49", "3.49", "6.99", "7.99", "8.99", "9.99", "9.49"]


def mergeFiles():
    #functions.merger(txt.get() + '.pdf', results)
    galleryfinal = []
    dailyfinal = []
    gallerylist = [line.rstrip('\n') for line in open("gallery_sorted.txt")]
    dailylist = [line.rstrip('\n') for line in open("daily_sorted.txt")]
    for gal in gallerylist:
        galleryfinal.append(functions.find_between(gal,"^","^"))
        print(functions.find_between(gal,"^","^"))
    for dai in dailylist:
        dailyfinal.append(functions.find_between(dai,"^","^"))
        print(functions.find_between(dai,"^","^"))
    functions.merger("Gallery_Sweet-" + foldername + '.pdf', galleryfinal)
    functions.merger("Daily-" + foldername + '.pdf', dailyfinal)
    messagebox.showinfo('MergeFiles', 'Done')

def checkDuplicates():
    location = filedialog.askopenfilename(initialdir=path.dirname(__file__),
                                           filetypes=(("Text Files", "*.txt"), ("all files", "*.*")))
    print(location)
    duplicates = [line.rstrip('\n') for line in open(location)]
    if functions.checkIfDuplicates(duplicates):
        messagebox.showinfo('Duplicates', 'Duplicates found')
    else:
        messagebox.showinfo('Duplicates', 'No duplicates found')

def loadandMerge():
    global foldername
    folder = filedialog.askdirectory(initialdir=path.dirname(__file__))
    messagebox.showinfo('Final Files', 'Select the output folder')
    output_folder = filedialog.askdirectory(initialdir=path.dirname(__file__))
    foldername = os.path.basename(folder)
    functions.scanDoublePages(folder, galleryprices, dailyprices)
    functions.sortFiles("gallery")
    functions.sortFiles("daily")
    functions.sortFiles("sweet")
    galleryfinal = []
    dailyfinal = []
    sweetlist = [line.rstrip('\n') for line in open("sweet_sorted.txt")]
    gallerylist = [line.rstrip('\n') for line in open("gallery_sorted.txt")]
    dailylist = [line.rstrip('\n') for line in open("daily_sorted.txt")]

    for gal in gallerylist:
        galleryfinal.append(functions.find_between(gal,"^","^"))
        print(functions.find_between(gal,"^","^"))
    for dai in dailylist:
        dailyfinal.append(functions.find_between(dai,"^","^"))
        print(functions.find_between(dai,"^","^"))
    functions.merger(output_folder + "/" + "Gallery-" + foldername + '.pdf', galleryfinal)
    functions.merger(output_folder + "/" + "Daily-" + foldername + '.pdf', dailyfinal)
    if not sweetlist:
        print("No Sweet Deals Only ")
    else:
        sweetfinal = []
        for swt in sweetlist:
            sweetfinal.append(functions.find_between(swt, "^", "^"))
            print(functions.find_between(swt, "^", "^"))
        functions.merger(output_folder + "/" + "Sweet-" + foldername + '.pdf', sweetfinal)
    messagebox.showinfo('Shirtpunch Miner', 'Process Done')
    #status.set('Opening the output folder...')
    webbrowser.open(os.path.realpath(output_folder))
    #status.set('Ready to Start!')


#text bar
#txt = Entry(window, width=30)
#txt.place(relx=0.5, rely=0.5, anchor=CENTER)
#buttons
#mergebtn = Button(window, text='Merge Files', command=mergeFiles)
#.place(relx=0.5, rely=0.65, anchor=CENTER)
#mergebtn['font'] = myFont
duplicatesbtn = Button(window, text='Check Duplicates', command=checkDuplicates)
duplicatesbtn.place(relx=0.5, rely=0.75, anchor=CENTER)
loadFilesMergebtn = Button(window, text='Load Files and Merge', command=loadandMerge)
loadFilesMergebtn['font'] = myFont
loadFilesMergebtn.place(relx=0.5, rely=0.40, anchor=CENTER)
#status = tk.StringVar(value="Ready to Start")
#statuslbl = Label(window, textvariable=status)
#statuslbl.place(relx=0.5, rely=0.55, anchor=CENTER)



window.mainloop()