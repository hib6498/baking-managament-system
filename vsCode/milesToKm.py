from tkinter import *

def milesToKm():
    Label3.config(text=f"{float(infield.get())*1.609}")
    
window = Tk()
window.title("Miles to Kilometers converter.")
window.minsize(width = 150, height = 90)

infield = Entry(width = 10)
infield.grid(row = 0, column = 1)

Label1 = Label(text = "Miles")
Label1.grid(row = 0, column = 2)

Label2 = Label(text = "is equal to")
Label2.grid(row = 1, column = 0)

Label3 = Label(text = "0")
Label3.grid(row = 1, column = 1)

Label4 = Label(text = "Km")
Label4.grid(row = 1, column = 2)

calcButton = Button(text="Calculate", command = milesToKm)
calcButton.grid(row = 2, column = 1)
window.mainloop()
