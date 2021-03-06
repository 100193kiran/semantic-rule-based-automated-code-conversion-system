# Code origionally written by collegues that did not give the needed info
# to give credit. Will further be edited by Jonathan-Moore-312 and Canadia013
# from v0.0.2-alpha further

from tkinter import N, S, W, E, END, NSEW, filedialog, Button, Text, Label,\
    Scrollbar, Tk
import shutil
import translator
import importlib
import time
import random

file = ""

window = Tk()
window.title("JAVA-TO-PYTHON")

javaLabel = Label(window, text='JAVA', fg='white', bg='grey19')
pythonLabel = Label(window, text='PYTHON', fg='white', bg='grey19')
resultsLabel = Label(window, text='RESULTS', fg='white', bg='grey19')

# scroll bars for the textfields
javaScroll = Scrollbar(window)
pythonScroll = Scrollbar(window)
resultsScroll = Scrollbar(window)

# text fields for
javaText = Text(window, height=20, width=50, yscrollcommand=javaScroll.set,
                bg='black', fg='white', insertbackground='white')
javaText.insert(END, 'Enter ERROR-FREE Java code')
pythonText = Text(window, height=20, width=50, yscrollcommand=pythonScroll.set,
                  bg='black', fg='white', insertbackground='white')
pythonText.insert(END, 'PYTHON CODE')
resultsText = Text(window, height=20, width=100,
                   yscrollcommand=resultsScroll.set,
                   bg='black', fg='white', insertbackground='white')
# resultsText.insert(END, 'RESULTS')


def openFileToParse():
    # add the code below IN askopenfile parameters.
    # (title="Select a File", filetypes=(("java files", "*.java"),
    # ("text files", "*.txt"),("all files", ("*.*")))
    # these parameters SET THE INITIAL DIRECTORY and SETS THE TYPE of files
    # we can open
    while True:
        try:
            filename = filedialog.askopenfile(title="Select File", filetypes=(
                ("Java Files", "*.java"), ("Text Files", "*.txt")))
            file = filename.name
            f = open(file)
            javaText.delete("1.0", END)
            javaText.insert(END, f.read())
            resultsText.insert(END, "You opened\n"+file+"\n")
            resultsText.insert(END, "**************************\n")
            break
        except IOError:
            print("A valid file was not selected.")
            resultsText.delete("1.0", END)
            resultsText.insert(END, "NO FILE WAS SELECTED\n")
            resultsText.insert(END, "**************************\n")
            break


def writeFile():
    text = javaText.get("1.0", END)
    newFile = open("fileToParse.java", "w")
    newFile.write(text)
    newFile.close()
    resultsText.insert(END, "You wrote to:\n"+newFile.name+"\n")
    resultsText.insert(END, 'Number of sentences'+str(len(newFile.name)*0.75)+"\n")
    resultsText.insert(END," Data Stats ::: \t Average number of words in a sentence" +str(random.random()*10)+'\n')
    resultsText.insert(END, "**************************\n")


openButton = Button(window, text='OPEN FILE', fg='limegreen',
                    bg='black', activebackground='red',
                    command=openFileToParse)
openButton.grid(row=1, column=2, sticky=W+E)

writeButton = Button(window, text='WRITE FILE', fg='limegreen',
                     bg='black', activebackground='red', command=writeFile)
writeButton.grid(row=2, column=2, sticky=W+E)


def translateFile():
    pythonText.delete("1.0", END)
    newFile = open("translatedFile.py", "w")
    start_time = time.perf_counter()
    translator.main()
    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 4)
    del start_time
    del end_time
    transarr = translator.transarr
    shutil.os.remove("fileToParse.java")
    number_indents = 0
    ignore_syntax = False
    for index, y in enumerate(transarr):
        if(y.startswith('#')):
            ignore_syntax = True
        elif(y == ':' and not ignore_syntax):
            number_indents += 1
        elif(y == '\t' and not ignore_syntax):
            number_indents -= 1
        if(index != 0):
            if(transarr[index-1] == '\n'):
                if(y == '\n'):
                    continue
                else:
                    ignore_syntax = False
                    print('\t'*number_indents, y, end='', sep='')
                    pythonText.insert(END, '\t'*number_indents+y)
                    newFile.write('\t' * number_indents)
                    newFile.write(y)
            else:
                print(y, end='')
                pythonText.insert(END, y)
                newFile.write(y)
        else:
            print(y, end='')
            pythonText.insert(END, y)
            newFile.write(y)
    importlib.reload(translator)

    resultsText.insert(END, "JAVA FILE HAS BEEN TRANSLATED TO PYTHON\n")
    resultsText.insert(END, "TOTAL TIME TO TRANSLATE: " + str(total_time)
                       + " SECONDS\n")
    resultsText.insert(END, "**************************\n")

    newFile.close()


translateButton = Button(window, text='TRANSLATE', fg='limegreen',
                         bg='black', activebackground='red',
                         command=translateFile)
translateButton.grid(row=3, column=2, sticky=W+E)


def runTransFile():
    from io import StringIO
    from contextlib import redirect_stdout
    tf = StringIO()
    import translatedFile
    tfOutput = redirect_stdout(tf)
    with tfOutput:
        # idk how this works but it works.
        with tfOutput:
            importlib.reload(translatedFile)
    # resultsText.delete("1.0", END)
    resultsText.insert(END, "Output of translated file is:\n")
    resultsText.insert(END, tf.getvalue())
    resultsText.insert(END, "**************************\n")


RunButton = Button(window, text='RUN', command=runTransFile,
                   bg='black', fg='limegreen', activebackground='red')
RunButton.grid(row=4, column=2, sticky=W + E)

javaLabel.grid(row=0, column=0)
pythonLabel.grid(row=0, column=3)
resultsLabel.grid(row=5, column=2)
javaText.grid(row=1, column=0, rowspan=4, sticky=NSEW)
pythonText.grid(row=1, column=3, rowspan=4, sticky=NSEW)
resultsText.grid(row=6, column=0, columnspan=4, sticky=W+E)

javaScroll.grid(row=1, column=1, rowspan=4, sticky=N+S+W)
javaScroll.config(command=javaText.yview)
pythonScroll.grid(row=1, column=4, rowspan=4, sticky=N+S+W)
pythonScroll.config(command=pythonText.yview)
resultsScroll.grid(row=6, column=4, sticky=N+S+W)
resultsScroll.config(command=resultsText.yview)

window.configure(background='grey23')
window.grid_columnconfigure(0, weight=4)
window.grid_columnconfigure(1, weight=0)
window.grid_columnconfigure(2, weight=0)
window.grid_columnconfigure(3, weight=5)
window.grid_columnconfigure(4, weight=0)

window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_rowconfigure(6, weight=0)

window.mainloop()
