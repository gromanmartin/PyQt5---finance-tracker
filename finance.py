import tkinter as tk 
from tkinter import ttk


root = tk.Tk()
root.geometry("750x400")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

mainFrame = tk.Frame(root)
mainFrame.grid(row=0, column=0, sticky='NSEW')
mainFrame.grid_rowconfigure(0, weight=1)
mainFrame.grid_columnconfigure(0, weight=1)

label1 = tk.Label(mainFrame, text='Welcome to your finance tracker', font=('Font',32))
label1.grid()

menuFrame = tk.Frame(root)
menuFrame.grid(row=1, column=0, sticky='NSEW', pady=50)
menuFrame.grid_rowconfigure(1, weight=1)
menuFrame.grid_columnconfigure(0, weight=1)

buttonStyle = ttk.Style()
buttonStyle.configure('A.TButton', width = 20, font=('',24))
button_login = ttk.Button(menuFrame, text='Login', style='A.TButton')
button_newacc = ttk.Button(menuFrame, text='Create new account', style='A.TButton')
button_exit = ttk.Button(menuFrame, text='Exit', style='A.TButton')

button_login.grid()
button_newacc.grid()
button_exit.grid()


root.mainloop()