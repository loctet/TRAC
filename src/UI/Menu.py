import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sys
import os
from TRAC.src.TransactionsGrinder import *

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("DAFSM Files", ".dafsm .txt")])
    
    if not filepath:
        return
    os.path.abspath(filepath)
    print(os.path.abspath(filepath), os.path.basename(filepath), os.path.dirname(filepath))
    
    messagebox.showinfo("File Opened", f"File {filepath} opened successfully!")
    #trGrinder = TransactionsGrinder(file_name, non_stop = args.non_stop == "1", time_out = args.time_out)

def save_file():
    messagebox.showinfo("Save DAFSM", "Saving File not implemented.")

def check_wellformness():
    messagebox.showinfo("Check Wellformness", "Wellformness checking not implemented.")

def visualize():
    messagebox.showinfo("Visualize", "Visualization not implemented.")

def generate_bulk():
    messagebox.showinfo("Bulk DAFSM", "Bulk generation not implemented.")

def import_bulk():
    messagebox.showinfo("Bulk Import", "Bulk import not implemented.")

def run_bulk():
    messagebox.showinfo("Run Bulk", "Run bulk not implemented.")

def plots_bulk():
    messagebox.showinfo("Plots Bulk", "Bulk plots not implemented.")

def create_main_menu(app):
    # Menu
    menu_bar = tk.Menu(app)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Import File", command=open_file)
    file_menu.add_command(label="Save DAFSM", command=save_file)
    file_menu.add_command(label="Load Image", command=load_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=app.quit)

    menu_bar.add_cascade(label="File", menu=file_menu)

    # Actions menu
    actions_menu = tk.Menu(menu_bar, tearoff=0)
    actions_menu.add_command(label="Check Wellformness", command=check_wellformness)
    actions_menu.add_command(label="Visualize", command=visualize)
    menu_bar.add_cascade(label="Actions", menu=actions_menu)

    # Bulk DAFSM menu
    bulk_menu = tk.Menu(menu_bar, tearoff=0)
    bulk_menu.add_command(label="Generate", command=generate_bulk)
    bulk_menu.add_command(label="Import", command=import_bulk)
    bulk_menu.add_command(label="Run", command=run_bulk)
    bulk_menu.add_command(label="Plots", command=plots_bulk)
    menu_bar.add_cascade(label="Bulk DAFSM", menu=bulk_menu)
    
    app.config(menu=menu_bar)


def load_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        return
    
    
    clear_frame(main_frame)

    # Tabbed Interface
    notebook = ttk.Notebook(main_frame)
    tab_image = ttk.Frame(notebook)
    tab_dafsm = ttk.Frame(notebook)
    notebook.add(tab_image, text='Image')
    notebook.add(tab_dafsm, text='DAFSM')
    notebook.pack(expand=True, fill='both')

    # Image Tab
    img_label = tk.Label(tab_image)
    img_label.pack(expand=True)

    # DAFSM Tab
    dafsm_label = tk.Label(tab_dafsm, text="DAFSM Model will be shown here.")
    dafsm_label.pack(expand=True)

    img = Image.open(filepath)
    #img = img.resize((250, 250))
    photo = ImageTk.PhotoImage(img)
    img_label.config(image=photo)
    img_label.image = photo  # keep a reference to prevent garbage collection


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

app = tk.Tk()
app.title("TRAC")
app.geometry("800x600")
app.minsize(400, 400)
create_main_menu(app)

# Main Zone Frame
main_frame = tk.Frame(app)
main_frame.pack(expand=True, fill='both')

# Welcome Label
welcome_label = tk.Label(main_frame, text="Welcome to TRAC, select a file or load an image.")
welcome_label.pack(expand=True)



app.mainloop()
