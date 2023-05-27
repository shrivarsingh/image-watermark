from os import close
import tkinter, math, os
from tkinter.constants import COMMAND
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
from tkinter import PhotoImage, filedialog
from PIL import Image, EpsImagePlugin, ImageTk

# Download and install ghostscript
EpsImagePlugin.gs_windows_binary =  r'C:\\Program Files\\gs\\gs9.55.0\\bin\\gswin64c.exe'

BUTTON_PADDING = 5
SML_BUTTON_WIDTH = 15
LRG_BUTTON_WIDTH = 30


def open_image():
    """Opens image

    Opens a file dialog to locate picture
    """
    
    global image_name
    # Grab File Name
    location_full_string = filedialog.askopenfilename(initialdir=".", title="Open File", filetypes=(("Image Files", "*.png"), ("All Files", "*.*")))
    pic_location = location_full_string.replace("C:/", "/")
    image_name = pic_location.split("/")[-1]
    display_image(picture_location=pic_location)


def save_image():
    """Saves canvas as an image

    Saves the canvas as an image by creating a temp.eps file and then converts the temp.eps into a png format picture
    """

    global image_name
     # Save the canvas as encapsulated postscript
    canvas.postscript(file="temp.eps")
    img = Image.open("temp.eps")
    image_name = "watermark_" + image_name
    if (image_name[-1:-5:-1] != "gnp."):
        image_name = image_name + ".png"
    img.save(image_name)


def close_application():
    """Closes the application

    Closes appliction and tries to delete temp.eps file that was created
    """

    if os.path.isfile("temp.eps"):
        try:
            os.remove("temp.eps")
        except PermissionError:
            print("Cannot delete temp files")
    window.destroy()


def watermark_text():
    """ Update watermark text

    Updates watermark text by using a string input dialog window
    """

    watermark_t = askstring('Text', 'Update Watermark Text:')
    canvas.itemconfig(image_text, text=watermark_t)


def watermark_size():
    """ Updates watermark size

    Updates watermark size by using an integer dialog window
    """

    watermark_s = askinteger('Size', 'Update Watermark Size:')
    canvas.itemconfig(image_text, font=("Courier", watermark_s, "bold"))


def watermark_colour():
    """Update watermark colour

    Updates watermark colour by using a dialog window
    """

    watermark_c = askcolor(title='Colour')
    canvas.itemconfig(image_text, fill=watermark_c[1])


def display_image(picture_location):
    """Updates canvas to a new picture
    
    Updates canvas to a new picture and rescales the picture and window

    Parameters
    ----------
    picture location : str
        full string of the location of the picture
    """

    img = (Image.open(picture_location))
    if (img.size[0] > 1200):
        scale_img = img.size[0] / 1200
        scale_img_width = math.ceil(img.size[0]/scale_img)
        scale_img_height = math.ceil(img.size[1]/scale_img)
        img = img.resize((scale_img_width, scale_img_height), Image.ANTIALIAS)
    elif (img.size[1] > 800):
        scale_img = math.ceil(img.size[1] / 800)
        scale_img_width = math.ceil(img.size[0]/scale_img)
        scale_img_height = math.ceil(img.size[1]/scale_img)
        img = img.resize((scale_img_width, scale_img_height), Image.ANTIALIAS)
    canvas.config(width=(img.size[0]), height=(img.size[1]))
    picture = ImageTk.PhotoImage(img)
    canvas.imageList.append(picture)
    canvas.itemconfig(photo, image=picture)
    canvas.coords(image_text, img.size[0]/2, img.size[1]/2)
    if (len(canvas.imageList) > 1):
        canvas.imageList.pop(0)


image_name = ""
window = tkinter.Tk()
window.title("Image Watermarking App")
window.config(padx=BUTTON_PADDING, pady=BUTTON_PADDING, background="black")

canvas = tkinter.Canvas(width=600, height=400, bg="#000000")
photo = canvas.create_image(0, 0, anchor="nw")
image_text = canvas.create_text(300, 200, text="Watermark", fill="white", font=("Courier", 35, "bold"))
canvas.imageList = []
canvas.grid(row=0, column=0, columnspan=4)

btn_open = tkinter.Button(text="Open Image", width=SML_BUTTON_WIDTH, command=open_image)
btn_open.grid(row=1, column=0, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

btn_text = tkinter.Button(text="Watermark Text", width=SML_BUTTON_WIDTH, command=watermark_text)
btn_text.grid(row=1, column=1, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

btn_size = tkinter.Button(text="Watermark Size", width=SML_BUTTON_WIDTH, command=watermark_size)
btn_size.grid(row=1, column=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

btn_colour = tkinter.Button(text="Watermark Colour", width=SML_BUTTON_WIDTH, command=watermark_colour)
btn_colour.grid(row=1, column=3, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

btn_save = tkinter.Button(text="Save Image", width=LRG_BUTTON_WIDTH, command=save_image)
btn_save.grid(row=2, column=0, columnspan=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

btn_exit = tkinter.Button(text="Exit", width=LRG_BUTTON_WIDTH, command=close_application)
btn_exit.grid(row=2, column=2, columnspan=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)

window.mainloop()