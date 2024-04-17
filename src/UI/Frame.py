import tkinter as tk
from tkinter import messagebox

def add_transition():
    messagebox.showinfo("Action", "Add Transition clicked.")

def check_well_formedness():
    messagebox.showinfo("Action", "Check Well Formedness clicked.")

def check_result():
    messagebox.showinfo("Action", "Check Result clicked.")

def view_fsm_image():
    messagebox.showinfo("Action", "View FSM Image clicked.")

# Create the main window
root = tk.Tk()
root.title("Title")

# Set the window size
root.geometry("400x300")

# Create a text box for JSON DAFSM display
text_box = tk.Text(root, height=10, width=50)
text_box.pack()

# Create buttons
btn_add_transition = tk.Button(root, text="ADD TRANSITION", command=add_transition)
btn_add_transition.pack()

btn_check_well_formedness = tk.Button(root, text="Check well formedness", command=check_well_formedness)
btn_check_well_formedness.pack()

btn_check_result = tk.Button(root, text="Check result", command=check_result)
btn_check_result.pack()

btn_view_fsm_image = tk.Button(root, text="VIEW FSM Image", command=view_fsm_image)
btn_view_fsm_image.pack()

# Run the application
root.mainloop()
