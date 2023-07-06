from tkinter import *
from tkinter import ttk 

#TODO Figure out how to have multiple displays.
titleDisplay:str = "N/A"
DescriptionDisplay:str = "No Json made or selected. Please Import one or click \"New JSON\""

def FormNewJson():
    newJsonInfo = Tk(className="New Json")
    popUp= ttk.Frame(newJsonInfo, padding=10)
    popUp.grid()
    ttk.Label(popUp, Text="Title of Game").grid(row=0)
    ttk.Label(popUp, Text ="Description").grid(row=1)
    title : Entry = ttk.Entry(popUp).grid(row=0,column=1)
    description: Entry = ttk.Entry(popUp).grid(row=1,column=1)
    ttk.Button(popUp, text="Done",command=lambda: CloseAndSaveJSON(title.get(), description.get(),popUp))
    popUp.mainloop()

def CloseAndSaveJSON(title:str, description:str, window:Frame):
    global titleDisplay
    global DescriptionDisplay
    titleDisplay = title
    DescriptionDisplay = description
    window.destroy()

about: str = """Welcome to Twitch plays any!\nHow to use: Form a JSON utilizing the key-capture tool below. You can also Import and Export your own."""
main = Tk(className="Main")
frm= ttk.Frame(main, padding=50)
frm.grid(padx=10,pady=10)
ttk.Label(frm, text=about).grid(column=0,row=0)
ttk.Widget(frm,"text").grid(column=0,row=1)
ttk.Button(frm, text="New JSON", command=FormNewJson ).grid(column=1, row=1)
ttk.Button(frm, text="Quit", command=main.destroy).grid(column=2,row=2)
main.mainloop()


