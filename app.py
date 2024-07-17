from PIL import Image, ImageOps, ImageFilter, ImageTk
from tkinter import filedialog

def add_image(canvas):
    filepath = filedialog.askopenfilename(
        initialdir="C:/Users/senit/Desktop/Opencv/Imageeditor")
    if filepath:
        image = Image.open(filepath)
        width, height = int(image.width / 2), int(image.height / 2)
        image = image.resize((width, height), Image.LANCZOS)
        canvas.config(scrollregion=(0, 0, image.width, image.height))
        canvas.image = ImageTk.PhotoImage(image)
        canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=canvas.image, anchor="center")

def auto_contrast(canvas):
    pass

def auto_sharpen(canvas):
    pass

def auto_cartoon(canvas):
    pass

def auto_invert(canvas):
    pass

def bypass_censorship(canvas):
    pass

def rotate_image(canvas):
    pass

def crop_image(canvas):
    pass

def change_brightness(canvas):
    pass

def change_contrast(canvas):
    pass

def change_saturation(canvas):
    pass

def apply_color_mask(canvas):
    pass

def detect_faces(canvas):
    pass