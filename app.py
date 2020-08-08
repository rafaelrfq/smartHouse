from pyswip import Prolog
from tkinter import *
from tkinter import messagebox
prolog = Prolog()
prolog.consult("file.pl")

# for value in prolog.query("shirt(X)"):
#     print(value["X"])

# Objects that will be shown in the list
objetosLista = []

# functions to make everything work
def realizarConsulta():
    if consultInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe escribir una consulta')
    else:
        resultado = list(prolog.query(str(consultInput.get())))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def popularLista():
    lista.delete(0, END)
    for o in objetosLista:
        lista.insert(END, o)

def clearInput():
    consultEntry.delete(0, END)

# create window object and give it a title
app = Tk()
app.title('Smart House')

# resize default size
app.geometry('800x400')

# consult field and label
consultLabel = Label(app, text='Consulta:', font=('bold', 14), pady=15, padx=3)
consultLabel.grid(row=0, column=0)
consultInput = StringVar()
consultEntry = Entry(app, textvariable=consultInput)
consultEntry.grid(row=0, column=1)

# consult button
consultBtn = Button(app, text='Consultar', command=realizarConsulta, pady=5)
consultBtn.grid(row=1, column = 3)

# list to show results
lista = Listbox(app, height=10, width=100)
lista.grid(row=3, column=1, columnspan=6, rowspan=10)

# Scrollbar for the list
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=7)

# Set scrollbar a la lista
lista.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=lista.yview)

# run app
app.mainloop()