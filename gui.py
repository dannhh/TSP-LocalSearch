# for GUI
from tkinter import Tk, Canvas, Entry, Text, Label, Button, PhotoImage, Toplevel, Entry, filedialog
from PIL import Image, ImageTk
#for GUI function 
from pathlib import Path
import numpy as np
import math
import random
import csv
import time
from tabu_search import tabu_search
from simulated_annealing import solver


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

simulated_annealing=0
tabu=1
#initial value
filename=""
d_mode=0
graph=[]
v=0
f=1
coor=[(0,0),(0,0)]
number_of_cities=0
cities_list=[]
cities=[]
algorithm=simulated_annealing#default algorithm
opt=2#default opt

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def add_image(path):
    img = Image.open(path)
    img = img.resize((int(img.size[0]*r_s), int(img.size[1]*r_s)))
    img = ImageTk.PhotoImage(img)
    return img
def create_rectangle(canvas, t, l, b, r, f, o):
    canvas.create_rectangle(int(t*r_s), int(l*r_s), int(b*r_s), int(r*r_s), fill=f, outline=o)
def create_text(canvas, x, y, a, t, f, font):
    canvas.create_text(int(x*r_s), int(y*r_s), anchor=a, text=t, fill=f, font=font)
def place(widget, x, y, w, h):
    widget.place(x=int(x*r_s), y=int(y*r_s), width=int(w*r_s), height=int(h*r_s))
def change_algorithm(simu_button_0, simu_button_1, tabu_button_0, tabu_button_1): #tabu_button_0, simu_button_0 are the chosen states of self.buttons
    global algorithm
    if algorithm==tabu:
        algorithm=simulated_annealing
        tabu_button_0.place_forget()
        place(tabu_button_1,1092.0,490.0,348.0,60.0)
        simu_button_1.place_forget()
        place(simu_button_0,1092.0,412.0,348.0,60.0)
    else:
        algorithm=tabu
        tabu_button_1.place_forget()
        place(tabu_button_0,1092.0,490.0,348.0,60.0)
        simu_button_0.place_forget()
        place(simu_button_1,1092.0,412.0,348.0,60.0)
def change_opt(opt2_button_0, opt2_button_1, opt3_button_0, opt3_button_1): #opt2_button_0, opt3_button_0 are the chosen states of self.buttons
    global opt
    if opt==2:
        opt=3
        opt2_button_0.place_forget()
        place(opt2_button_1,1183.0,568.0,257,60)
        opt3_button_1.place_forget()
        place(opt3_button_0,1183.0,646.0,257,60)
    else:
        opt=2
        opt2_button_1.place_forget()
        place(opt2_button_0,1183.0,568.0,257,60)
        opt3_button_0.place_forget()
        place(opt3_button_1,1183.0,646.0,257,60)
#multiple_list all element of a list with n
def multiple_list(lst,n):
    return [x * n for x in lst]
    
class App:
    def __init__(self):
        self.root = Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        global r_s
        r_s=min(w/1440,h/1024)*0.9 #resize scale

        #Input window
        self.canvas = Canvas(
            self.root,
            bg = "#FFFFFF",
            height = 1024*r_s,
            width = 1440*r_s,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        #add image
        self.button_image_12 = add_image(relative_to_assets("button_12.png"))
        self.button_image_14 = add_image(relative_to_assets("button_14.png"))
        self.button_12 = Button(
            image=self.button_image_12,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.visualize_csv_input(),
            relief="flat"
        )
        self.button_14 = Button(
            image=self.button_image_14,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.visualize_selfdrawing_input(),
            relief="flat"
        )
        
    def display(self):
        self.root.geometry('%dx%d+0+0' % (1440*r_s,1024*r_s))
        self.root.configure(bg = "#FFFFFF")
        self.canvas.place(x = 0, y = 0)
        create_text(self.canvas,697.0,480.0,"nw","Input","#669F82",("Rubik Medium", int(18 * r_s)))
        place(self.button_12,550.0,519.0,135.0,50.0)
        place(self.button_14,755.0,519.0,135.0,50.0)
        self.root.resizable(False, False)
        self.root.mainloop()
    def visualize_csv_input(self):
        global filename
        filename =filedialog.askopenfilename()
        global v
        v=1
        draw=self.drawing_window(self.root)
        draw.display()
    def visualize_selfdrawing_input(self):
        global v
        v=0
        draw=self.drawing_window(self.root)
        draw.display()
    class drawing_window:
        def __init__(self, root):
            if v==1 and filename=="": return
            self.window=Toplevel(root)
            #Canvas
            self.canvas = Canvas(
                self.window,
                bg = "#FFFFFF",
                height = 1024*r_s,
                width = 1440*r_s,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )
            self.drawing_canvas= Canvas(
                self.window,
                bg = "#FFFFFF",
                height = int(1024*r_s*0.75),
                width = int(1440*r_s*0.75),
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )
            #add image
            self.button_image_1 = add_image(relative_to_assets("button_1.png"))
            self.button_image_2 = add_image(relative_to_assets("button_2.png"))
            self.button_image_3 = add_image(relative_to_assets("button_3.png"))
            self.button_image_4 = add_image(relative_to_assets("button_4.png"))
            self.button_image_5 = add_image(relative_to_assets("button_5.png"))
            self.button_image_6 = add_image(relative_to_assets("button_6.png"))
            self.button_image_7 = add_image(relative_to_assets("button_7.png"))
            self.button_image_8 = add_image(relative_to_assets("button_8.png"))
            self.button_image_9 = add_image(relative_to_assets("button_9.png"))
            self.button_image_15 = add_image(relative_to_assets("button_15.png"))
            self.button_image_16 = add_image(relative_to_assets("button_16.png"))
            self.city=add_image(relative_to_assets("city30.png"))
            self.c_size=self.city.height()#as city is a square image
            
            self.button_1 = Button(self.window,
                image=self.button_image_1,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_opt(self.button_2, self.button_1, self.button_4, self.button_3),
                relief="flat"
            )

            
            self.button_2 = Button(self.window,
                image=self.button_image_2,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_opt(self.button_2, self.button_1, self.button_4, self.button_3),
                relief="flat"
            )
            
            self.button_3 = Button(self.window,
                image=self.button_image_3,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_opt(self.button_2, self.button_1, self.button_4, self.button_3),
                relief="flat"
            )
            
            self.button_4 = Button(self.window,
                image=self.button_image_4,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_opt(self.button_2, self.button_1, self.button_4, self.button_3),
                relief="flat"
            )
            
            self.button_5 = Button(self.window,
                image=self.button_image_5,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_algorithm(self.button_6, self.button_5, self.button_8, self.button_7),
                relief="flat"
            )
            
            self.button_6 = Button(self.window,
                image=self.button_image_6,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_algorithm(self.button_6, self.button_5, self.button_8, self.button_7),
                relief="flat"
            )
            
            self.button_7 = Button(self.window,
                image=self.button_image_7,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_algorithm(self.button_6, self.button_5, self.button_8, self.button_7),
                relief="flat"
            )
            
            self.button_8 = Button(self.window,
                image=self.button_image_8,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: change_algorithm(self.button_6, self.button_5, self.button_8, self.button_7),
                relief="flat"
            )
            
            self.button_9 = Button(self.window,
                image=self.button_image_9,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.run(),
                relief="flat"
            )
            
            self.button_15 = Button(self.window,
                image=self.button_image_15,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.change_draw_mode(drawing_canvas),
                relief="flat"
            )
            
            self.button_16 = Button(self.window,
                image=self.button_image_16,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.draw_city(),
                relief="flat"
            )
        def display(self):
            self.window.geometry('%dx%d+0+0' % (1440*r_s,1024*r_s))
            self.canvas.place(x = 0, y = 0)
            self.drawing_canvas.place(x = int(75*r_s), y = int(75*r_s))
            
            #place self.button
            place(self.button_2,1183.0,568.0,257,60)
            place(self.button_3,1183.0,646.0,257,60)
            place(self.button_6,1092.0,412.0,348.0,60.0)
            place(self.button_7,1092.0,490.0,348.0,60.0)
            place(self.button_9,1242.0,7.0,106.0,60.0)
            #if input is self-drawing                    
            if v==0:
                place(self.button_15,12.0,110.0,50.0,50.0)
            if v==0:
                place(self.button_16,12.0,185.0,50.0,50.0)
            #Rectangle
            create_rectangle(self.canvas,0.0,75.0,75.0,1024.0,"#FFCC5C","")
            create_rectangle(self.canvas,0.0,0.0,1440.0,75.0,"#88D8B0","")
            create_rectangle(self.canvas,75.0,874.0,1440.0,1024.0,"#FFEEAD","")
            #Text
            create_text(self.canvas,105.0,890.0,"nw","Tour cost:","#669F82",("Rubik Medium", int(30 * r_s)))
            create_text(self.canvas,105.0,935.0,"nw","Tour path:","#669F82",("Rubik Medium", int(30 * r_s)))
            create_text(self.canvas,50.0,17.0,"nw","Travelling saleman problem","#F9F9F9",("Rubik Black", int(36 * r_s)))
            #if input is csv file
            if v==1:
                global graph
                graph = np.loadtxt(filename, delimiter=",")
                size=len(graph)
                global vertices
                vertices=list(zip(multiple_list(random.sample(range(0,size*2),size),int(1440*r_s*0.75/(size*2))),
                                    multiple_list(random.sample(range(0,size*2),size),int(1024*r_s*0.75/(size*2)))))
                for i in range (0,size):
                    self.add_city_path(vertices, graph)                            
            self.window.resizable(False, False)
            self.window.mainloop()
        def run(self):
            global tour, cost, v, f
            tour=[]
            cost=0
            if algorithm==tabu:
                tour, cost = tabu_search(graph,opt)
            else:
                tour, cost = solver(graph,opt)
            v=2
            f=1
            c_label = Label(self.window, text=cost, fg="#669F82", bg="#FFEEAD",font=("Rubik Medium", int(30 * r_s)))
            c_label.place(x=305.0*r_s,y=890.0*r_s)
            t_label = Label(self.window, text=tour, fg="#669F82", bg="#FFEEAD",font=("Rubik Medium", int(30 * r_s)))
            t_label.place(x=305.0*r_s,y=935.0*r_s)
            t_length=len(tour)
            for i in range(t_length):
                self.add_path(vertices[tour[i]],tour[i])
                time.sleep(0.5)
                if i+1 in range(t_length):
                    self.add_path(vertices[tour[i+1]],tour[i+1])
                    time.sleep(0.5)
        def add_city(self, event):
            global number_of_cities, vertices
            cities_list.append((event.x, event.y))
            cities.append(Button(self.drawing_canvas,
                image=self.city,
                text=number_of_cities,
                width=self.c_size,
                height=self.c_size,
                borderwidth=0,
                highlightthickness=0,
                compound="center",
                command=lambda c=(event.x-15*r_s,event.y-15*r_s), n=number_of_cities:
                                    [self.add_path(c,n), vertices.append(event.x,event.y)]
            ))
            cities[number_of_cities].place(x=event.x-15*r_s, y=event.y-15*r_s)
            number_of_cities+=1
            graph.append([])
            for i in range(number_of_cities-1):
                graph[i].append(999999)
            for i in range(number_of_citieSs):
                graph[number_of_cities-1].append(999999)
        def add_city_path(self,vertices, graph):
            global number_of_cities
            number_of_cities=len(vertices)
            for i in range (number_of_cities):
                cities.append(Button(self.drawing_canvas,
                    image=self.city,
                    text=i,
                    width=self.c_size,
                    height=self.c_size,
                    borderwidth=0,
                    highlightthickness=0,
                    compound="center"
                    )
                )
                cities[i].place(x=int(vertices[i][0]-15*r_s), y=int(vertices[i][1]-15*r_s))
                """for j in range(number_of_cities):
                    if i==j: break
                    inter_point=(vertices[i][0],vertices[j][1])
                    canvas.create_line(vertices[i], inter_point ,vertices[j], width=1, arrow = "last", smooth=1)
                    canvas.create_text(coor[0][0], coor[1][1],text=graph[i][j])"""

        def draw_city(self):
            self.drawing_canvas.update()
            if d_mode==0:
                self.canvas.bind("<Button>",lambda event: self.add_city(event))
                self.canvas.place()
        def change_draw_mode(self):
            global d_mode, graph
            if d_mode==0:
                d_mode=1
                self.unbind("<Button>")
                self.place()
        def take_input(ec_window, self, text):
            global graph
            graph[no2][no1]=text.get(1.0,"end-1c")
            self.drawing_canvas.create_text(coor[0][0], coor[1][1],text=graph[no2][no1])
            if graph[no2][no1]=='':
                graph[no2][no1]=999999
            else:
                graph[no2][no1]=int(graph[no2][no1])
            ec_window.destroy()
            ec_window.update()
        def enter_cost(self):
            print(1)
            ec_window=Toplevel(self.window)
            ec_window.geometry('%dx%d+%d+%d' % (500*r_s,125*r_s,470*r_s,424*r_s))
            ec_canvas = Canvas(
                ec_window,
                bg = "#FFFFFF",
                height = 125*r_s,
                width = 500*r_s,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge"
            )

            ec_canvas.place(x = 0, y = 0)
            create_text(ec_canvas,25.0,5.0,"nw",
                        "Enter the cost of travelling from city "+ str(no1) +" to city "+ str(no2),
                        "#669F82",("Rubik Black", int(18 * r_s)))
            text=Text(ec_canvas)
            place(text,200.0,35.0,100,30)
            enter=Button(ec_canvas, text="Enter", command= lambda:take_input(ec_window, self,text))
            place(enter,200.0,65.0,100,30)
            
        def add_path(self,c,n):
            if d_mode or v==2:
                global f
                global coor
                global no1, no2
                if f:
                    coor[0]=c
                    no1=n
                    f=0
                elif c!=coor[0]:
                    coor[1]=c
                    no2=n
                    inter_point=(coor[0][0],coor[1][1])
                    if v==0:
                        self.drawing_canvas.create_line(coor[0], inter_point ,coor[1], width=1, arrow = "last", smooth=1)
                        self.drawing_canvas.bind("<Expose>",enter_cost(canvas))
                    if v==2:
                        self.drawing_canvas.create_line(coor[0], inter_point ,coor[1], width=1, fill="#FF6F69", arrow = "last", smooth=1)
                        self.drawing_canvas.update()
                    f=1
app=App()
app.display()
