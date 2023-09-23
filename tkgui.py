from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText  
import threading
import json
from pynput import keyboard, mouse
#Creating a new Object for keyboard capture. Naming it as such
class KeyboardCapture:
    #Key is a weird type that is included in keyboard. Look for it.
    def start(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=None) as self.listener:
            self.listener.join()


    def end(self):
        #Terminate existing listener
        self.listener.stop()


    def on_press(self, key: keyboard.Key):
        try:
            #Alphanumeric keys go here!

            #TODO  Replace this with actions.
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            #Special keys go here.
            print('special key {0} pressed'.format(key)) 



titleDisplay:str = None
DescriptionDisplay:str = None
class App:
    def __init__(self) -> None:
        self.t1 = threading.Thread(target=self.FormNewJsonWindow)
        self.main = Tk(className="Main") #Run Main HERE So we can access the main thread elsewhere throughout the object
        self.MadeJson: dict[str, any] = {}
        self.WindowLaunch()
        self.showJson: Text #Defined in "WindowLaunch"


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
        #Now Write to ShowJson
        self.showJson.config(state=NORMAL)
        self.showJson.delete("1.0",END)
        self.showJson.insert("1.0",json.dumps(self.MadeJson))
        self.showJson.config(state=DISABLED)


    def WindowLaunch(self) -> None: 
        about: str = """Welcome to Twitch plays any!
        How to use: Form a JSON utilizing the key-capture tool below. You can also Import and Export your own. Once you make a new JSON it will appear in the text field below.
        NOTE: The text field below is not editable. If you wish to edit the JSON directly simply open it in notepad."""
        frm= ttk.Frame(self.main, padding=50)
        frm.grid(padx=10,pady=10)
        ttk.Label(frm, text=about).grid(column=0,row=0)
        self.showJson:Text = Text(frm)
        self.showJson.grid(column=0,row=1)
        self.showJson.insert("1.0",json.dumps(self.MadeJson))
        self.showJson.config(state=DISABLED)
        print(json.dumps(self.MadeJson))
        ttk.Button(frm, text="New JSON", command=self.FormNewJson ).grid(column=0, row=2)
        ttk.Button(frm, text="Quit", command=self.main.destroy).grid(column=1,row=2)
        self.main.mainloop()


#Next I need to capture keys in order for this to work.
#Learn how the keyboard listener works. Once I figure this out. I can capture keys,
#Making it easy for people to use.


def Main():
    #instance:App = App()
    listener:KeyboardCapture = KeyboardCapture()


Main()