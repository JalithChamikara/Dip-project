from random import randint
from tkinter import filedialog, ttk
from PIL import Image, ImageTk,ImageOps
import cv2
import numpy as np
from image_operations import (
    change_brightness, change_contrast
)

def add_image(canvas):
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if not file_path:
        return

    # Load the image using PIL
    pil_image = Image.open(file_path)
    
    # Store the original image to reset modifications
    canvas.original_image = pil_image.copy()
    
    # Resize image to fit into canvas while maintaining aspect ratio
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    pil_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
    
    canvas.image = ImageTk.PhotoImage(pil_image)

    # Clear the canvas and add the image
    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")

def auto_invert(canvas):
    # Auto invert the image
 if hasattr(canvas, 'original_image'):
        pil_image = canvas.original_image.copy()
        inverted_image = ImageOps.invert(pil_image)

        # Resize inverted image to fit into canvas while maintaining aspect ratio
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        inverted_image.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

        canvas.image = ImageTk.PhotoImage(inverted_image)
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image  # Maintain reference to avoid garbage collection
        canvas.update_idletasks()  # Force canvas update

def bypass_censorship(canvas):
    # Function to bypass censorship
     if hasattr(canvas, 'image'):
        pil_image = canvas.original_image.copy()
        pil_image = pil_image.convert("RGB")  # Ensure the image is in RGB mode
        pixel_data = pil_image.load()
        width, height = pil_image.size

        # Iterate over each pixel in the image
        for y in range(height):
            for x in range(width):
                # Get the RGB values of the pixel
                r, g, b = pixel_data[x, y]

                # Check if the pixel is censored (e.g., black pixel)
                if r == 0 and g == 0 and b == 0:
                    # Replace the censored pixel with a random color
                    r = randint(0, 255)
                    g = randint(0, 255)
                    b = randint(0, 255)

                    # Update the pixel data
                    pixel_data[x, y] = (r, g, b)

        # Update the canvas image
        canvas.image = ImageTk.PhotoImage(pil_image)
        canvas.delete("all")
        canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, image=canvas.image, anchor="center")
        canvas.image_reference = canvas.image  # Maintain reference to avoid garbage collection
        canvas.update_idletasks()  # Force canvas update

def crop_image(canvas):
    # Function to crop image
    pass

def change_saturation(canvas):
    # Function to change saturation
    pass

def apply_color_mask(canvas):
    # Function to apply color mask
    pass


def detect_faces(canvas):
    print("Detecting faces...")
    if not hasattr(canvas, 'original_image'):
        return

    pil_image = canvas.original_image.convert('RGB')
    open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        return

    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(open_cv_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    pil_image_with_faces = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    pil_image_with_faces.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

    canvas.image = ImageTk.PhotoImage(pil_image_with_faces)
    canvas.delete("all")
    canvas.create_image(canvas_width // 2, canvas_height // 2, image=canvas.image, anchor="center")
    canvas.image_reference = canvas.image
    canvas.update_idletasks()


def show_brightness_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    brightness_slider, brightness_value_label, reset_brightness_button, save_brightness_button = sliders["brightness"]
    brightness_slider.pack(side="left", padx=20)
    brightness_value_label.pack(side="left", padx=10)
    reset_brightness_button.pack(side="left", padx=10)
    save_brightness_button.pack(side="left", padx=10)
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)
    brightness_slider.bind("<Motion>", lambda event: update_brightness_value(canvas, brightness_slider, brightness_value_label))

def show_contrast_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    contrast_slider, contrast_value_label, reset_contrast_button, save_contrast_button = sliders["contrast"]
    contrast_slider.pack(side="left", padx=20)
    contrast_value_label.pack(side="left", padx=10)
    reset_contrast_button.pack(side="left", padx=10)
    save_contrast_button.pack(side="left", padx=10)
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)
    contrast_slider.bind("<Motion>", lambda event: update_contrast_value(canvas, contrast_slider, contrast_value_label))

def update_brightness_value(canvas, brightness_slider, brightness_value_label):
    brightness_value = brightness_slider.get()
    brightness_value_label.config(text=str(int(brightness_value)))
    change_brightness(canvas, brightness_value)

def update_contrast_value(canvas, contrast_slider, contrast_value_label):
    contrast_value = contrast_slider.get()
    contrast_value_label.config(text=str(int(contrast_value)))
    change_contrast(canvas, contrast_value)


def reset_brightness(canvas, brightness_slider, brightness_value_label):
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)

def reset_contrast(canvas, contrast_slider, contrast_value_label):
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)

def save_current_edit(canvas):
    if hasattr(canvas, 'image'):
        canvas.current_image = ImageTk.getimage(canvas.image)    




def show_brightness_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    brightness_slider, brightness_value_label, reset_brightness_button, save_brightness_button = sliders["brightness"]
    brightness_slider.pack(side="left", padx=20)
    brightness_value_label.pack(side="left", padx=10)
    reset_brightness_button.pack(side="left", padx=10)
    save_brightness_button.pack(side="left", padx=10)
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)
    brightness_slider.bind("<Motion>", lambda event: update_brightness_value(canvas, brightness_slider, brightness_value_label))

def show_contrast_controls(canvas, bottom_frame, sliders):
    if not bottom_frame.winfo_ismapped():
        bottom_frame.pack(side="bottom", fill="x", pady=10)
    for slider, label, reset_button, save_button in sliders.values():
        slider.pack_forget()
        label.pack_forget()
        reset_button.pack_forget()
        save_button.pack_forget()
    contrast_slider, contrast_value_label, reset_contrast_button, save_contrast_button = sliders["contrast"]
    contrast_slider.pack(side="left", padx=20)
    contrast_value_label.pack(side="left", padx=10)
    reset_contrast_button.pack(side="left", padx=10)
    save_contrast_button.pack(side="left", padx=10)
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)
    contrast_slider.bind("<Motion>", lambda event: update_contrast_value(canvas, contrast_slider, contrast_value_label))

def update_brightness_value(canvas, brightness_slider, brightness_value_label):
    brightness_value = brightness_slider.get()
    brightness_value_label.config(text=str(int(brightness_value)))
    change_brightness(canvas, brightness_value)

def update_contrast_value(canvas, contrast_slider, contrast_value_label):
    contrast_value = contrast_slider.get()
    contrast_value_label.config(text=str(int(contrast_value)))
    change_contrast(canvas, contrast_value)


def reset_brightness(canvas, brightness_slider, brightness_value_label):
    brightness_slider.set(50)
    brightness_value_label.config(text="50")
    change_brightness(canvas, 50)

def reset_contrast(canvas, contrast_slider, contrast_value_label):
    contrast_slider.set(50)
    contrast_value_label.config(text="50")
    change_contrast(canvas, 50)

def save_current_edit(canvas):
    if hasattr(canvas, 'image'):
        canvas.current_image = ImageTk.getimage(canvas.image)    