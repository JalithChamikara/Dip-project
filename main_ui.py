import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET

def create_widget(parent, element):
    widget = None
    attribs = element.attrib

    if element.tag == "label":
        if "name" in attribs and attribs["name"] in ["image_edit", "image_thumbnail"]:
            try:
                img = Image.open("thumbnail.jpg")  # Open the image using PIL
                if attribs["name"] == "image_edit":
                    img = img.resize((512, 512))  # Resize the image to fit the label (adjust as necessary)
                elif attribs["name"] == "image_thumbnail":
                    img = img.resize((150, 150))  # Resize the image to fit the label (adjust as necessary)
                img = ImageTk.PhotoImage(img)  # Convert to ImageTk format
                widget = tk.Label(parent, image=img, bg=attribs.get("bg", "#ffffff"))
                widget.image = img  # Keep a reference to the image to avoid garbage collection
            except Exception as e:
                print(f"Error loading image: {e}")
                widget = tk.Label(parent, text="Image not found", bg=attribs.get("bg", "#ffffff"))
        else:
            widget = tk.Label(parent, text=attribs.get("text", ""), bg=attribs.get("bg", "#ffffff"))
    elif element.tag == "button":
        widget = tk.Button(parent, text=attribs.get("text", ""), bg=attribs.get("bg", "#ffffff"), fg=attribs.get("fg", "#000000"))
    elif element.tag == "frame":
        widget = tk.Frame(parent, name=attribs.get("name", ""), bg=attribs.get("bg", "#ffffff"))
    elif element.tag == "scale":
        widget = tk.Scale(parent, from_=int(attribs.get("from", 0)), to=int(attribs.get("to", 100)), orient=attribs.get("orient", "horizontal"), bg=attribs.get("bg", "#ffffff"))
    elif element.tag == "panedwindow":
        widget = tk.PanedWindow(parent, orient=attribs.get("orient", tk.HORIZONTAL), bg=attribs.get("bg", "#ffffff"))

    if widget:
        if "side" in attribs:
            widget.pack(side=attribs["side"], fill=attribs.get("fill", tk.NONE), expand=attribs.get("expand", "no") == "yes")
        else:
            widget.pack()

    return widget

def build_ui_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    window_attrib = root.find("window").attrib
    window = tk.Tk()
    window.title(window_attrib["title"])
    window.geometry(f'{window_attrib["width"]}x{window_attrib["height"]}')
    window.configure(bg=window_attrib.get("bg", "#ffffff"))
    
    def create_widgets(parent, elements):
        for element in elements:
            widget = create_widget(parent, element)
            if list(element):
                create_widgets(widget, list(element))

    create_widgets(window, list(root.find("window")))
    
    return window

if __name__ == "__main__":
    window = build_ui_from_xml("main_ui.xml")
    window.mainloop()
