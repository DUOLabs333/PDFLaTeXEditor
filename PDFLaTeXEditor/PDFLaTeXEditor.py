importDir=r"C:\Users\School\Downloads"
exportDir=r"C:\Users\School\Downloads"
#pdf2cairoPath=r"C:\Users\School\Downloads\PDFLaTeXEditor\poppler-0.68.0_x86\poppler-0.68.0\bin\pdftocairo.exe"
libPath=r"C:\Users\School\Downloads\PDFLaTeXEditor\lib"
inkscapePath=r"C:\Users\School\Downloads\PDFLaTeXEditor\inkscape-1.0.1-x64\inkscape\bin\inkscape.exe"
drawPath=r"C:\Users\School\Downloads\PDFLaTeXEditor\LibreOfficePortable\LibreOfficeDrawPortable.exe"

Stringify=lambda string: '"'+string+'"'
Join=lambda directory,file: directory+r'\ '[:-1]+file

#Dependencies:

from tkinter import *
from tkinter import filedialog,messagebox
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import shutil
import zipfile
from pathlib import Path
import subprocess
from PIL import Image, ImageTk
from functools import partial

tk = Tk()
filenameDisplay=StringVar(tk)
filenameDisplay.set("")
numPages=StringVar(value=["Page 1"])
tk.title("New Document - PDFLaTeXEditor")

def resetChdir():
    os.chdir(str(Path.home()))


def pdf2duo(file):
    newpath=Join(importDir,file.split(r'\ '[:-1])[-1][:-4])
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    f=open(file,"rb")
    inputpdf = PdfFileReader(f)

    global numPages
    numPages.set(["Page "+str(_+1) for _ in range(inputpdf.numPages)])

    with open(Join(newpath,"numPages.txt"),"w") as numPagesFile:
        numPagesFile.write(str(inputpdf.numPages))
        
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(Join(newpath,"page_"+str(i+1)+".pdf"), "wb") as outputStream:
            output.write(outputStream)

        #subprocess.call(Stringify(pdf2cairoPath)+" -pdf "+Stringify(Join(newpath,"page_"+str(i+1)+".pdf"))+" "+Stringify(Join(importDir,"pdf.pdf")),creationflags=0x08000000)

        subprocess.call(Stringify(inkscapePath)+" "+Stringify(Join(newpath,"page_"+str(i+1)+".pdf"))+" --export-filename="+Join(importDir,"pdf"+".pdf"),creationflags=0x08000000)
        shutil.move(Join(importDir,"pdf"+".pdf"),Join(newpath,"page_"+str(i+1)+".pdf"))

        subprocess.call(Stringify(inkscapePath)+" "+Stringify(Join(newpath,"page_"+str(i+1)+".pdf"))+" --export-filename="+Stringify(Join(newpath,"page_"+str(i+1)+".svg")),creationflags=0x08000000)

        os.remove(Join(newpath,"page_"+str(i+1)+".pdf"))
        #subprocess.call(Stringify(inkscapePath)+" "+Stringify(Join(newpath,"page_"+str(i+1)+".pdf"))+" --export-filename="+Stringify(Join(newpath,"page_"+str(i+1)+".png"))+" --export-background-opacity=255",creationflags=0x08000000)

#If Inkscape doesn't embed, use pdftocairo
#Double click to open in LibreOffice Draw, and install mathstex in a portable version. Can open it and save it
    f.close()
    
    os.chdir(importDir)
    shutil.make_archive(file.split(r'\ '[:-1])[-1][:-4],'zip',file.split(r'\ '[:-1])[-1][:-4])
    resetChdir()
    
    os.rename(file[:-4]+".zip",os.path.splitext(file[:-4]+".zip")[0]+".duo")
    shutil.rmtree(newpath)



size=(0,0)
def viewPage(file,num):
##    os.rename(file,os.path.splitext(file)[0]+".zip")
##    with zipfile.ZipFile(os.path.splitext(file)[0]+".zip") as z:
##        with open(Join(exportDir,"svg_temp.png"), "wb") as f:
##            f.write(z.read("page_"+str(num)+".png"))
##
##    os.rename(os.path.splitext(file)[0]+".zip",os.path.splitext(file)[0]+".duo")

    subprocess.call(Stringify(inkscapePath)+" "+Stringify(Join(file[:-4],"page_"+str(num)+".svg"))+" --export-filename="+Stringify(Join(importDir,"png_temp.png"))+" --export-background-opacity=255",creationflags=0x08000000)    
    img = Image.open(Join(exportDir,"png_temp.png"))

    global size
    size = img.size

    pimg = ImageTk.PhotoImage(img)

    os.remove(Join(exportDir,"png_temp.png"))

    
    return pimg

pimg=viewPage(Join(libPath,'blank.duo'),1)

frame = Canvas(tk, width=size[0], height=size[1])
frame.pack()
frame.create_image(0,0,anchor='nw',image=pimg)



pages = Canvas(tk)
images = Canvas(tk)


buttonWidth=5

def LoadPic(file,scale,event=None):
    filename=Join(libPath,file)
    img=Image.open(filename)
    pass
    
def Load(event=None):

    global filename
    filename_temp=filedialog.askopenfilename(initialdir=importDir,filetypes=(("DUO files","*.duo"),("PDF files","*.pdf")))
    if(len(filename_temp)>0):
        filename = filename_temp
        filename = filename.replace(r"/ "[:-1],r"\ "[:-1])
        filenameDisplay.set(filename.split(r"\ "[:-1])[-1])

def Open(event=None):
    
    global pimg
    if not os.path.isfile(os.path.splitext(filename)[0]+".duo"):
        pdf2duo(filename)
        os.rename(os.path.splitext(filename)[0]+".duo",os.path.splitext(filename)[0]+".zip")
    else:
        os.rename(os.path.splitext(filename)[0]+".duo",os.path.splitext(filename)[0]+".zip")
        with zipfile.ZipFile(os.path.splitext(filename)[0]+".zip") as z:
            with z.open("numPages.txt") as f:
                for line in f:
                    global numPages
                    numPages.set(["Page "+str(_+1) for _ in range(int(line))])

        #os.rename(os.path.splitext(filename)[0]+".zip",os.path.splitext(filename)[0]+".duo")
    with zipfile.ZipFile(os.path.splitext(filename)[0]+".zip",'r') as z:
        z.extractall(os.path.splitext(filename)[0])                    

    os.remove(os.path.splitext(filename)[0]+".zip")
    tk.title(str(filenameDisplay.get())[:-3]+"duo"+" - PDFLaTeXEditor")
    filenameDisplay.set("")
    pimg=viewPage(os.path.splitext(filename)[0]+".duo",1)
    frame = Canvas(tk, width=size[0], height=size[1])
    frame.place(x=tk.winfo_screenwidth()//2,y=0,anchor="n")
    frame.create_image(0,0,anchor='nw',image=pimg)
        
    pages.place(x=0,y=0,height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)
    images.place(x=0,y=tk.winfo_screenwidth(),height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)

    listbox.select_set(0)

def SelectPage(event=None):
    global pimg
    pimg=viewPage(filename[:-3]+"duo",listbox.curselection()[0]+1)
    frame = Canvas(tk, width=size[0], height=size[1])
    frame.place(x=tk.winfo_screenwidth()//2,y=0,anchor="n")
    frame.create_image(0,0,anchor='nw',image=pimg)
        
    pages.place(x=0,y=0,height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)

def OpenPage(event=None):
    #print("Hello")
    subprocess.call(Stringify(drawPath)+" "+Join(os.path.splitext(filename)[0],"page_"+str(listbox.curselection()[0]+1)+".svg"))

#If the window is closed, save the file as .duo, then close (same as "Save")-- https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter

def OnEntryUpDown(self, event):
    selection = event.widget.curselection()[0]
    
    if event.keysym == 'Up':
        selection += -1

    if event.keysym == 'Down':
        selection += 1

    if 0 <= selection < event.widget.size():
        event.widget.selection_clear(0, tk.END)
        event.widget.select_set(selection)

def Save(event=None):
    file=filename
    os.chdir(importDir)
    shutil.make_archive(file.split(r'\ '[:-1])[-1][:-4],'zip',file.split(r'\ '[:-1])[-1][:-4])
    resetChdir()

    os.rename(file[:-4]+".zip",os.path.splitext(file[:-4]+".zip")[0]+".duo")
    shutil.rmtree(file[:-4])

    global pimg
    pimg=viewPage(Join(libPath,'blank.duo'),1)
    
    frame = Canvas(tk, width=size[0], height=size[1])
    frame.place(x=tk.winfo_screenwidth()//2,y=0,anchor="n")
    frame.create_image(0,0,anchor='nw',image=pimg)

    pages.place(x=0,y=0,height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)
    images.place(x=0,y=tk.winfo_screenwidth(),height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)

    listbox.select_set(0)

    numPages=1
    tk.title("New Document - PDFLaTeXEditor")

def Export(event=None):
    file=filedialog.asksaveasfilename(initialdir=exportDir)
    if(len(file)>0):
        file = file.replace(r"/ "[:-1],r"\ "[:-1])
        if(messagebox.askyesno("Confirm Decision",'Are you sure you want to save '+Stringify(filename.split(r"\ "[:-1])[-1][:-3]+"duo")+' as '+Stringify(file.split(r"\ "[:-1])[-1]))+"?"):
            merger=PdfFileMerger()
            with open(Join(os.path.splitext(filename)[0],"numPages.txt")) as f:
                for line in f:
                    numPages=int(line)
                        
            for i in range(1,numPages+1):
                subprocess.call(Stringify(inkscapePath)+" "+Stringify(Join(filename[:-4],"page_"+str(i)+".svg"))+" --export-filename="+Stringify(Join(filename[:-4],"page_"+str(i)+".pdf")),creationflags=0x08000000)
                merger.append(Join(filename[:-4],"page_"+str(i)+".pdf"))
                
            merger.write(file)
            merger.close()

            for i in range(1,numPages+1):
                os.remove(Join(filename[:-4],"page_"+str(i)+".pdf"))
    

def on_closing():
    if len(filename)>0:
        file=filename
        os.chdir(importDir)
        shutil.make_archive(file.split(r'\ '[:-1])[-1][:-4],'zip',file.split(r'\ '[:-1])[-1][:-4])
        resetChdir()

        os.rename(file[:-4]+".zip",os.path.splitext(file[:-4]+".zip")[0]+".duo")
        shutil.rmtree(file[:-4])
        tk.destroy()     

loadOpen=Frame(pages)

Button(loadOpen, text='Load', command=Load,width=buttonWidth).pack(side=LEFT)
Button(loadOpen,text="Open",command=Open, width=buttonWidth).pack(side=LEFT)
Label(loadOpen,textvariable=filenameDisplay,relief="sunken",anchor="w").pack(side=LEFT,fill=BOTH,expand=1)

loadOpen.pack(side=TOP,anchor="w",fill=X)

pages.place(x=0,y=0,height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)

List=Frame(pages)

listbox = Listbox(List,listvariable=numPages,exportselection=False,selectmode=SINGLE)
listbox.pack(side = LEFT, fill = BOTH,expand=1)

scrollbar = Scrollbar(List)
scrollbar.pack(side = LEFT, fill = BOTH)

listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)

List.place(x=0, y=50,relwidth=1.0)

listbox.select_set(0)
listbox.bind('<<ListboxSelect>>',SelectPage)
listbox.bind('<Control-o>',OpenPage)
##listbox.bind('<Up>',OnEntryUpDown)
##listbox.bind('<Down>',OnEntryUpDown)



addRemove=Frame(images)
Button(addRemove,text='Add',width=buttonWidth).pack(side=LEFT)
addRemove.pack(side=TOP,anchor="e",fill=X)
images.place(x=tk.winfo_screenwidth(),y=0,height=tk.winfo_screenheight(), width=tk.winfo_screenwidth()//2-size[0]//2)

saveExport=Frame(pages)
Button(saveExport,text="Save",command=Save).pack(side=LEFT,fill=BOTH,expand=1)
Button(saveExport,text="Export",command=Export).pack(side=RIGHT,fill=BOTH,expand=1)
saveExport.place(x=0,y=25,relwidth=1.0)

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()
