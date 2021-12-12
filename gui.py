import tkinter as tk
from tkinter.constants import W
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import os 
from get_word import write_latex as wl
version="1.0"

# scriptpath = os.path.abspath(__file__) # get the complete absolute path to this script
#  scriptdir = os.path.dirname(scriptpath) # strip away the file name
#  imagepath = os.path.join(scriptdir, "specification.gif")

class GUI():
    def __init__(self,master) -> None:
        self.root=master
    def initial_window(self):
        self.root.title("单词本生成器_"+version)
        self.root.geometry('1068x681+10+10')
        self.button_start=tk.Button(self.root,text="开始",command=self.start_window).pack()
        self.button_cancel=tk.Button(self.root,text="退出",command=self.cancel).pack()
        self.button_speci=tk.Button(self.root,text="说明",command=self.specify_window).pack()
    def start_window(self):
        self.start_window=tk.Toplevel(self.root)
        self.start_window.geometry('1068x681+10+10')

        self.var_tex=tk.IntVar()
        self.var_pdf=tk.IntVar()

        self.button_import=tk.Button(self.start_window,text="浏览",command=self.import_file)
        self.scroller = ScrolledText(self.start_window)
        self.button_run=tk.Button(self.start_window,text="运行",command=self.run)
        self.check_tex=tk.Checkbutton(self.start_window,text="tex文件",variable=self.var_tex)
        self.check_pdf=tk.Checkbutton(self.start_window,text="pdf文件",variable=self.var_pdf)

        self.button_import.pack()
        self.scroller.pack(anchor='n',side=tk.LEFT,expand=True)
        self.button_run.pack(expand=True)
        self.check_tex.pack(anchor='n',side=tk.RIGHT)
        self.check_pdf.pack(anchor='n',side=tk.RIGHT)
    def cancel(self):
        self.root.destroy()
    def specify_window(self):
        self.specify_window=tk.Toplevel(self.root)
        self.specify_window.geometry('1068x681+10+10')

        self.specify=tk.Label(self.specify_window,text="说明").pack()
        photo_specify=tk.PhotoImage(file="specification.gif")
        self.specify=tk.Label(self.specify_window,image=photo_specify).pack()
    def import_file(self):
        file=filedialog.askopenfile(filetype=[('txt','TXT')])
        words=file.read().split(",")
        self.scroller.insert(tk.INSERT, words)
    def run(self):
        words=self.scroller.get()
        wl(words=words,tex=self.var_tex.get(),pdf=self.var_pdf.get())

def GUI_start():
    root=tk.Tk()#This could be specified to optimize the GUI.
    app_class=GUI(root)
    app_class.initial_window()
    root.mainloop()


GUI_start()