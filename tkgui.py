from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText  
import threading
import json
#TODO Figure out how to have multiple displays.
#Solution. Create Multiple threads using python threads.
#ISSUES: For some god damn reason my python interpriter really hates widget types form tkinter. Why? No idea.
# Right now the compiler is saying they are "None_Type" why? who tf knows...
# SOLVED: Python takes last function evaluated type in this case. grid() as seen in function "FormNewJsonWindow(Self)"
titleDisplay:str = None
DescriptionDisplay:str = None
class App:
    def __init__(self) -> None:
        self.t1 = threading.Thread(target=self.FormNewJsonWindow)
        self.main = Tk(className="Main") #Run Main HERE So we can access the main thread elsewhere throughout the object
        self.MadeJson: dict[str, any] = {}
        self.WindowLaunch()
        


    def FormNewJsonWindow(self) -> None:
        newJsonInfo = Tk(className="New Json")
        popUp= ttk.Frame(newJsonInfo, padding=25)
        popUp.grid()
        ttk.Label(popUp, text="Title").grid(row=0)
        ttk.Label(popUp, text="Description").grid(row=1)
        title : ttk.Entry = ttk.Entry(popUp)
        title.grid(row=0,column=1)
        description: ttk.Entry = ttk.Entry(popUp)
        description.grid(row=1,column=1)
        DoneButton: ttk.Button = ttk.Button(popUp, text="Done",command=lambda: self.CloseAndSaveJSON(title.get(), description.get(),window=newJsonInfo))
        DoneButton.grid(row=2,column=1)
        popUp.mainloop() 


    def FormNewJson(self):
        self.t1.run()

    def CloseAndSaveJSON(self, title:str, description:str, window:Tk):
        self.MadeJson={"Title": title, "Description": description, "Controls": {}}
        window.destroy()
        print(self.MadeJson)
        #Write Made Json to a file.
        with open(f"{self.MadeJson['Title']}.json", "w") as f:
            f.write(json.dumps(self.MadeJson))
            f.close()
        



    def WindowLaunch(self) -> None: 
        about: str = """Welcome to Twitch plays any!\n
        How to use: Form a JSON utilizing the key-capture tool below. You can also Import and Export your own. Once you make a new JSON it will appear in the text field below.\n
        NOTE: The text field below is not editable. If you wish to edit the JSON directly simply open it in notepad."""
        frm= ttk.Frame(self.main, padding=50)
        frm.grid(padx=10,pady=10)
        ttk.Label(frm, text=about).grid(column=0,row=0)
        #TODO Change this widget to be READONLY and 
        ttk.Label(frm, text=json.dumps(self.MadeJson), background="white", width=25).grid(column=0,row=1)
        ttk.Button(frm, text="New JSON", command=self.FormNewJson ).grid(column=1, row=1)
        ttk.Button(frm, text="Quit", command=self.main.destroy).grid(column=2,row=2)
        self.main.mainloop()






def Main():
    instance:App = App()


Main()