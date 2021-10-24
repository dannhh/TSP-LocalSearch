
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import numpy as np
import math
import random

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Entry, filedialog
from PIL import Image, ImageTk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


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
def change_algorithm(simu_button_0, simu_button_1, tabu_button_0, tabu_button_1): #tabu_button_0, simu_button_0 are the chosen states of buttons
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
def change_opt(opt2_button_0, opt2_button_1, opt3_button_0, opt3_button_1): #opt2_button_0, opt3_button_0 are the chosen states of buttons
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
def multiple(lst,n):
    return [x * n for x in lst]
def _draw_regular_polygon(canvas, center, radius, n, angle, **kwargs):
        angle -= (math.pi/n)
        coord_list = [[center[0] + radius * math.sin((2*math.pi/n) * i - angle),
            center[1] + radius * math.cos((2*math.pi/n) * i - angle)] for i in range(n)]
        return canvas.create_polygon(coord_list, **kwargs)
v=0
def visualize_input():
    global filename
    filename =filedialog.askopenfilename()
    global v
    v=1
    detail()
"""def close():
    create_rectangle(canvas, 0, 0, 1440, 1024, "#FFFFFF", "")
    create_text(canvas,697.0,480.0,"nw","Input","#669F82",("Rubik Medium", int(18 * r_s)))
    path_entry.place_forget()
    enter.place_forget()
    button_10.place_forget()
    place(button_12,550.0,519.0,135.0,50.0)
    place(button_14,755.0,519.0,135.0,50.0)"""
city_x=0
city_y=0
def add_city(event):
    global city_x, city_y
    city_x, city_y = event.x, event.y
#def run():
#    return
#detail_window
def detail():
    if v and filename=="": return
    window=Toplevel(root)
    
    window.geometry('%dx%d+0+0' % (1440*r_s,1024*r_s))
    #Canvas
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 1024*r_s,
        width = 1440*r_s,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    drawing_canvas= Canvas(
        window,
        bg = "#FFFFFF",
        height = int(1024*r_s*0.75),
        width = int(1440*r_s*0.75),
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    drawing_canvas.place(x = int(75*r_s), y = int(75*r_s))

    #Button
    global button_image_1
    button_image_1 = add_image(relative_to_assets("button_1.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_opt(button_2, button_1, button_4, button_3),
        relief="flat"
    )

    global button_image_2
    button_image_2 = add_image(relative_to_assets("button_2.png"))
    button_2 = Button(window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_opt(button_2, button_1, button_4, button_3),
        relief="flat"
    )

    global button_image_3
    button_image_3 = add_image(relative_to_assets("button_3.png"))
    button_3 = Button(window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_opt(button_2, button_1, button_4, button_3),
        relief="flat"
    )

    global button_image_4
    button_image_4 = add_image(relative_to_assets("button_4.png"))
    button_4 = Button(window,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_opt(button_2, button_1, button_4, button_3),
        relief="flat"
    )

    global button_image_5
    button_image_5 = add_image(relative_to_assets("button_5.png"))
    button_5 = Button(window,
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_algorithm(button_6, button_5, button_8, button_7),
        relief="flat"
    )

    global button_image_6
    button_image_6 = add_image(relative_to_assets("button_6.png"))
    button_6 = Button(window,
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_algorithm(button_6, button_5, button_8, button_7),
        relief="flat"
    )

    global button_image_7
    button_image_7 = add_image(relative_to_assets("button_7.png"))
    button_7 = Button(window,
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_algorithm(button_6, button_5, button_8, button_7),
        relief="flat"
    )
    
    global button_image_8
    button_image_8 = add_image(relative_to_assets("button_8.png"))
    button_8 = Button(window,
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: change_algorithm(button_6, button_5, button_8, button_7),
        relief="flat"
    )

    global button_image_9
    button_image_9 = add_image(relative_to_assets("button_9.png"))
    button_9 = Button(window,
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: run(),
        relief="flat"
    )

    global button_image_15
    button_image_15 = add_image(relative_to_assets("button_15.png"))
    button_15 = Button(window,
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_15 clicked"),
        relief="flat"
    )

    global button_image_16
    button_image_16 = add_image(relative_to_assets("button_16.png"))
    button_16 = Button(window,
        image=button_image_16,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_16 clicked"),
        relief="flat"
    )
    #place button
    place(button_2,1183.0,568.0,257,60)

    place(button_3,1183.0,646.0,257,60)

    place(button_6,1092.0,412.0,348.0,60.0)

    place(button_7,1092.0,490.0,348.0,60.0)

    place(button_9,1242.0,7.0,106.0,60.0)

    place(button_15,12.0,110.0,50.0,50.0)

    place(button_16,12.0,185.0,50.0,50.0)

    #Rectangle
    create_rectangle(canvas,0.0,75.0,75.0,1024.0,"#FFCC5C","")

    create_rectangle(canvas,0.0,0.0,1440.0,75.0,"#88D8B0","")

    create_rectangle(canvas,75.0,874.0,1440.0,1024.0,"#FFEEAD","")

    #create_rectangle(canvas, 520.0,424.0, 920.0, 599.0, "#FFFFFF", "#FFCC5C")

    #create_rectangle(canvas, 520.0, 424.0, 920.0, 474.0, "#88D8B0", "")

    #Text
    create_text(canvas,105.0,891.0,"nw","Tour cost:","#669F82",("Rubik Medium", int(30 * r_s)))

    #create_text(canvas,540.0,439.0,"nw","Travelling saleman problem","#FFFFFF",("Rubik Black", int(18 * r_s)))

    create_text(canvas,105.0,931.0,"nw","Tour path:","#669F83",("Rubik Medium", int(30 * r_s)))

    create_text(canvas,50.0,17.0,"nw","Travelling saleman problem","#F9F9F9",("Rubik Black", int(36 * r_s)))

    if v:
        graph = np.loadtxt(filename, delimiter=",")
        size=len(graph)
        vertices=list(zip(multiple(random.sample(range(0,size*2),size),int(1440*r_s*0.75/(size*2))),
                          multiple(random.sample(range(0,size*2),size),int(1024*r_s*0.75/(size*2)))))
        print(vertices)
        drawing_canvas.create_polygon(vertices, fill="#FFFFFF", outline="#000000")
    else: 
        drawing_canvas.bind("<Button-1>",add_city)
        drawing_canvas.place()
        
        drawing_canvas.create_image(city_x, city_y, image = city)
    window.resizable(False, False)
    window.mainloop()
root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
r_s=min(w/1440,h/1024)*0.9 #fit screen width, height

city=add_image(relative_to_assets("city30.png"))

root.geometry('%dx%d+0+0' % (1440*r_s,1024*r_s))
root.configure(bg = "#FFFFFF")
simulated_annealing=0
tabu=1
algorithm=simulated_annealing#default algorithm
opt=2#default opt

#Input window
canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 1024*r_s,
    width = 1440*r_s,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
create_text(canvas,697.0,480.0,"nw","Input","#669F82",("Rubik Medium", int(18 * r_s)))

button_image_10= add_image(relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: close(),
    relief="flat"
)

button_image_12 = add_image(relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: visualize_input(),
    relief="flat"
)

button_image_14 = add_image(relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: detail(),
    relief="flat"
)

place(button_12,550.0,519.0,135.0,50.0)

place(button_14,755.0,519.0,135.0,50.0)

root.resizable(False, False)
root.mainloop()
