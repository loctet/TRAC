import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sys
import os
import io
from TransactionsGrinder import *
from The_Validator import *
from Visual_graph import generate_visual_fsm

trGrinder = False
transition_template = {
    "start" : "_ {True} o:O > starts(c) {} {} S0",
    "normal" : "S0 {True} o > c.action() {} S1",
    "new_p" : "S0 {True} p:P > c.action() {} S1",
    "any_p" : "S0 {True} any p:P > c.action() {} S1",
    "final" : "S0 {True} o > c.action() {} S1+"
}
app = tk.Tk()
app.title("TRAC")
app.geometry("800x600")
app.minsize(400, 400)


# Main Zone Frame
main_frame = tk.Frame(app)
main_frame.pack(expand=True, fill='both')

# Welcome Label
welcome_label = tk.Label(main_frame, text="Welcome to TRAC, select a file or load an image.")
welcome_label.pack(expand=True)


def make_scrollable(frame, parent):
    # Create a canvas and two scrollbars to slide through the frame.
    canvas = tk.Canvas(parent)
    v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    # Place the scrollable frame on the canvas
    scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # This function updates the scroll region and possibly the size of the inner frame
    def on_frame_configure(event):
        # Reset the scroll region to encompass the inner frame
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def on_canvas_configure(event):
        # Ensure the inner frame's width is adjusted to the canvas size
        canvas.itemconfig(scrollable_frame_id, width=event.width)

    # Bind the Frame and Canvas configure events
    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    # Configure the canvas to properly use the scrollbars
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Pack everything correctly
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    return scrollable_frame


def file_get_content(file_path):
    content = ""
    # Open the file using 'with' statement to ensure it gets closed after reading
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def open_file():
    global trGrinder

    filepath = filedialog.askopenfilename(filetypes=[("DAFSM Files", ".dafsm .txt")])
    
    if not filepath:
        return
    file_name = os.path.splitext(os.path.basename(filepath))[0]
    file_dir = os.path.dirname(filepath)
    trGrinder = TransactionsGrinder(
        file_name, 
        non_stop = True, 
        time_out = 0,
        txt_path = file_dir,
        z3model_path = os.path.join(file_dir, "Z3_model"),
        json_path = os.path.join(file_dir, "json_model")
    )
    sParser = The_Validator()
    sParser.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())
        
    generate_visual_fsm(trGrinder.get_full_json_path(), trGrinder.get_full_png_path())
    load_image(trGrinder.get_full_png_path(), file_get_content(filepath))

def save_file():
    alert("Save DAFSM", "Saving File not implemented.")

def check_wellformness():
    if not trGrinder:
        alert("Check Wellformness", "No DAFSM Imported")
        return
    trGrinder.get_json_from_file()
    trGrinder.pre_process_fsm()

    # Create a StringIO object to capture output
    output = io.StringIO()

    # Save the original stdout
    original_stdout = sys.stdout
    sys.stdout = output

    trGrinder.tr_grinding(True)
    # Restore stdout to its original setting
    sys.stdout = original_stdout

    # Get the content from the StringIO object
    captured_output = output.getvalue()

    # Close the StringIO object
    output.close()
    message_to_frame(captured_output)

    

def visualize():
    if not trGrinder: 
        alert("Visualize", "No model loaded.")
        return
    load_image(trGrinder.get_full_png_path(), file_get_content(trGrinder.get_full_txt_path()))
    

def alert(title = "Alert" , mesage = "Message"):
    messagebox.showinfo(title, mesage)

def generate_bulk():
    alert("Bulk DAFSM", "Bulk generation not implemented.")

def import_bulk():
    alert("Bulk Import", "Bulk import not implemented.")

def run_bulk():
    alert("Run Bulk", "Run bulk not implemented.")

def plots_bulk():
    alert("Plots Bulk", "Bulk plots not implemented.")

def create_main_menu(app):
    # Menu
    menu_bar = tk.Menu(app)

    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Import File", command=open_file)
    file_menu.add_command(label="Save DAFSM", command=save_file)
    file_menu.add_command(label="Edit DAFSM", command=load_image(None, ""))
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

def check_format():
    content = text_area.get("1.0", tk.END)
    if not content.strip():
        return
    global trGrinder
    file_name = "temp_file"
    file_dir = "./Examples/FromUI"
    trGrinder = TransactionsGrinder(
        file_name, 
        non_stop = True, 
        time_out = 0,
        txt_path = file_dir,
        z3model_path = os.path.join(file_dir, "Z3_model"),
        json_path = os.path.join(file_dir, "json_model")
    )

    with open(trGrinder.get_full_txt_path(), 'w') as file:
        file.write(content)

    
    sParser = The_Validator()
    sParser.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())

    generate_visual_fsm(trGrinder.get_full_json_path(), trGrinder.get_full_png_path())
    load_image(trGrinder.get_full_png_path(), file_get_content(trGrinder.get_full_txt_path()))

def on_text_scroll(*args):
    line_numbers.yview(*args)
    text_area.yview(*args)

def on_mousewheel(event):
    text_area.yview_scroll(int(-1*(event.delta/120)), "units")

def update_line_numbers(event=None):
    line_numbers.delete("1.0", "end")
    current = text_area.index("@1,0")
    while True:
        dline = text_area.dlineinfo(current)
        if dline is None: break
        y = dline[1]
        linenum = str(current).split(".")[0]
        line_numbers.insert("end", linenum + "\n")
        current = text_area.index("%s+1line" % current)

def load_image(filepath, content):
    if not filepath:
        filepath = "./images/default.png"
    
    clear_frame(main_frame)

    # Tabbed Interface
    notebook = ttk.Notebook(main_frame)
    tab_image = ttk.Frame(notebook)
    scrollable_frame = make_scrollable(tab_image, tab_image)

    tab_code = ttk.Frame(notebook)
    notebook.add(tab_image, text='Image')
    notebook.add(tab_code, text='DAFSM Editor')
    notebook.pack(expand=True, fill='both')

    # Image Tab
    img = Image.open(filepath)
    img = img.resize((400, 400))  # Resize the image to better fit the display
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(scrollable_frame, image=photo)
    img_label.image = photo  # keep a reference to prevent garbage collection
    img_label.pack(expand=True, fill='both')



    # Code Editor Tab
    global text_area
    global line_numbers
    text_scrollbar = ttk.Scrollbar(tab_code)
    text_area = tk.Text(tab_code,  wrap='word', undo=True)
    text_scrollbar.config(command=on_text_scroll)
    text_scrollbar.pack(side="right", fill="y")
    text_area.pack(fill="both", expand=True)

    # Line numbers
    # line_numbers = tk.Text(tab_code, width=4, bg="gray", fg="white", state="disabled")
    # line_numbers.pack(side="left", fill="y")
    # text_area.bind("<MouseWheel>", on_mousewheel)
    # text_area.bind("<KeyRelease>", update_line_numbers)

    # Populate text area
    text_area.insert("1.0", content)
    # update_line_numbers()

    
    # Buttons under the textarea
    btn_frame = tk.Frame(tab_code)
    btn_frame.pack(side='top', fill='x', pady=10)
    for key in transition_template.keys() :
        func = globals()[f'add_transition_{key}']
        # Create a button and add it to the frame
        function = f"add_transition_{key}"
        ttk.Button(btn_frame, text=f"Add {key} Transition", command=func).pack(pady=10, side="left")  # Add padding around the button inside the frame

    ttk.Button(btn_frame, text=f"Visualize", command=check_format).pack(pady=10, side="left")  # Add padding around the button inside the frame

    


def add_transition_start():
    text = (text_area.get(1.0, "end-1c"))
    if text.strip() and text.find("_ ") > 0 :
        alert(mesage="Start transition already added")
        return
    transition_type = "start"
    index = text_area.index("insert")
    text_area.insert(index, f"# Added {transition_type} Transition here\n{transition_template[transition_type]}\n")
    
def add_transition_normal():
    transition_type = "normal"
    index = text_area.index("insert")
    text_area.insert(index, f"# Added {transition_type} Transition here\n{transition_template[transition_type]}\n")

def add_transition_new_p():
    transition_type = "new_p"
    index = text_area.index("insert")
    text_area.insert(index, f"# Added {transition_type} Transition here\n{transition_template[transition_type]}\n")

def add_transition_any_p():
    transition_type = "any_p"
    index = text_area.index("insert")
    text_area.insert(index, f"# Added {transition_type} Transition here\n{transition_template[transition_type]}\n")

def add_transition_final():
    transition_type = "final"
    index = text_area.index("insert")
    text_area.insert(index, f"# Added {transition_type} Transition here\n{transition_template[transition_type]}\n")


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def message_to_frame(message):
    clear_frame(main_frame)# Welcome Label
    m_label = tk.Label(main_frame, text = message)
    m_label.pack(expand=True)



create_main_menu(app)
app.mainloop()
