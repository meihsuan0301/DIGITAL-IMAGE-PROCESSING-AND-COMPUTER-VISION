import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk,Image
import numpy as np
#import os
#from os import listdir
import numpy as np
import cv2
from utils import *
import utils
# import matplotlib
from PIL import Image, ImageTk
from PIL.Image import fromarray
import matplotlib.pyplot as plt
#plt.switch_backend('agg')

class UI_Window:
    def __init__(self, name='UI'):
        self.name = name
        self.window = tk.Tk()
        
        self.window.title('image transfers')
        self.window.geometry('700x700')
        
        self.canvas = tk.Canvas(self.window, width=700, height=630, bg="white")
        self.canvas.place(x=0, y=70)
        
        self.label = tk.Label(self.window, text='請輸入參數:')
        self.label.place(x=400, y=0)

        self.parameter = tk.Text(self.window, width=20, height=1)
        self.parameter.place(x=400, y=20)
        
        self.menubar = Menu(self.window)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open Image", command=self.open_img)
        # file_menu.add_command(label="Save Image", command=save_image)
        #self.file_menu.add_separator()
        # file_menu.add_command(label="Exit", command=gui.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.opr_menu = Menu(self.menubar, tearoff=0)
        self.opr_menu.add_command(label="10pixel", command=self.transfer_funs('10pixel'))
        self.opr_menu.add_separator()
        self.opr_menu.add_command(label="log", command=self.transfer_funs('log'))
        self.opr_menu.add_command(label="gamma", command=self.transfer_funs('gamma'))
        self.opr_menu.add_command(label="negative", command=self.transfer_funs('negative'))
        self.opr_menu.add_separator()
        self.opr_menu.add_command(label="bilinear", command=self.transfer_funs('bilinear'))
        self.opr_menu.add_command(label="nearest", command=self.transfer_funs('nearest'))
        self.menubar.add_cascade(label="Operation", menu=self.opr_menu)
        self.window.config(menu=self.menubar)
        
#         self.btn = tk.Button(self.window, text='open image', command=self.open_img)
#         self.btn.place(x=0, y=0)
    
    

    def open_img(self):
        #filename = filedialog.askopenfilename(title='open')
        filename = filedialog.askopenfile(mode='r')
        fileType = filename.name.split('.')[-1]
        if fileType == 'raw':
            img = np.fromfile(filename.name, dtype=np.uint8).reshape(512, 512)
            self.img = Image.fromarray(img)      
        else:
            self.img = Image.open(filename.name)
    
#     def save_img(self):
#         imgPath = filedialog.asksaveasfile()
#         path = imgPath.name
#         self.img.save(path)
            
        #img = img.resize((250, 250), Image.ANTIALIAS)
#         self.img = ImageTk.PhotoImage(self.img)
#         panel = Label(self.window, image = self.img)
#         panel.image = self.img
        imgCanvas = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgCanvas)
        self.canvas.image = imgCanvas
        
        
            
    def transfer_funs(self, t):
            def transfer_fun():
                if t == '10pixel':
                    trans = pixel10
                    para = {}
                    
                if t == 'log':
                    trans = Log_tranfrom
                    para = {'c': float(self.parameter.get(1.0, tk.END))}

                if t == 'gamma':
                    trans = gamma_trans
                    para = {'gamma': float(self.parameter.get(1.0, tk.END))}

                if t == 'negative':
                    trans = negative_tranfrom
                    para = {}

                if t == 'bilinear':
                    trans = Bilinear_interpolation
                    p = self.parameter.get(1.0, tk.END).split(',')
                    p = list(map(int, p))
                    para = {'new_size': p}

                if t == 'nearest':
                    trans = Nearest_neighbor_interpolation
                    p = self.parameter.get(1.0, tk.END).split(',')
                    p = list(map(int, p))
                    para = {'new_size': p}
                    
                img = np.asarray(self.img).astype('float')
                img = trans(img = img, **para)
                img = np.uint8(img)
                self.img = Image.fromarray(img)
                imgCanvas = ImageTk.PhotoImage(self.img)
                image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=imgCanvas)
                self.canvas.image = imgCanvas
            return transfer_fun
        
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    window = UI_Window()
    window.run()