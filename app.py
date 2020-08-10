from pyswip import Prolog
from tkinter import *
from tkinter import messagebox
prolog = Prolog()
prolog.consult("smart_house.pl")

# for value in prolog.query("shirt(X)"):
#     print(value["X"])

# Objects that will be shown in the list
objetosLista = []

# functions to make everything work
def realizarConsulta():
    if consultInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir una consulta')
    else:
        resultado = list(prolog.query(str(consultInput.get())))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def agregarDispositivo():
    if dispInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un dispositivo en el campo')
    else:
        print(list(prolog.query("agregar_dispositivo(%s)" % dispInput.get())))
        resultado = list(prolog.query("dispositivo(X)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def agregarLugar():
    if lugarInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar en el campo')
    else:
        print(list(prolog.query("agregar_lugar(%s)" % lugarInput.get())))
        resultado = list(prolog.query("lugar(X)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def agregarDispLugar():
    if dispInput.get() == '' or lugarInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un dispositivo y un lugar en los campos')
    else:
        print(list(prolog.query("agregar_disp_lugar(%s, %s)" % (dispInput.get(), lugarInput.get()) )))
        resultado = list(prolog.query("dispositivo_lugar(Dispositivo, Lugar)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def popularLista():
    lista.delete(0, END)
    for o in objetosLista:
        lista.insert(END, o)
    objetosLista.clear()

def clearInput():
    consultEntry.delete(0, END)
    dispEntry.delete(0, END)
    lugarEntry.delete(0, END)

def secondWindow():
    second = Toplevel()
    second.geometry('640x480')
    label = Label(second, text='Ejemplo').pack()

# create window object and give it a title
app = Tk()
app.title('Smart House')
app.iconbitmap('D:/Projects/Django-Python/Prolog/house.ico')

# add background image
# C = Canvas(top, bg="blue", height=250, width=300)
bgimg = PhotoImage(file = "D:/Projects/Django-Python/Prolog/background.png")
bg_label = Label(app, image=bgimg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# resize default size
app.geometry('800x400')

# consult field and label
consultLabel = Label(app, text='Consulta:', font=('bold', 14), bg="black", fg="white")
consultLabel.grid(row=0, column=0)
consultInput = StringVar()
consultEntry = Entry(app, textvariable=consultInput)
consultEntry.grid(row=0, column=1)

# consult button
consultBtn = Button(app, text='Consultar', command=realizarConsulta, pady=3)
consultBtn.grid(row=1, column = 0)

# agregar_dispositivo field and label
dispLabel = Label(app, text='Dispositivo:', font=('bold', 14), bg="black", fg="white")
dispLabel.grid(row=0, column=2)
dispInput = StringVar()
dispEntry = Entry(app, textvariable=dispInput)
dispEntry.grid(row=0, column=3)

# agregar_dispositivo button
dispBtn = Button(app, text='Agregar Dispositivo', command=agregarDispositivo)
dispBtn.grid(row=1, column = 2, pady=10)

# agregar_lugar field and label
lugarLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
lugarLabel.grid(row=0, column=4)
lugarInput = StringVar()
lugarEntry = Entry(app, textvariable=lugarInput)
lugarEntry.grid(row=0, column=5)

# agregar_lugar button
lugarBtn = Button(app, text='Agregar Lugar', command=agregarLugar)
lugarBtn.grid(row=1, column = 4, pady=10)

# agregar_disp_lugar button
dispLugarBtn = Button(app, text='Agregar Disp. a Lugar', command=agregarDispLugar)
dispLugarBtn.grid(row=1, column = 6, pady=10)

# list to show results
lista = Listbox(app, height=8, width=100, setgrid=0)
lista.grid(row=2, column=1, columnspan=6, rowspan=8, pady=25)

# Scrollbar for the list
scrollbar = Scrollbar(app)
scrollbar.grid(row=2, column=6, pady=25)

# Set scrollbar a la lista
lista.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=lista.yview)

# second window button
secondWinBtn = Button(app, text='Abrir otra ventana', command=secondWindow, pady=5)
secondWinBtn.grid(row=13, column = 3)

# run app
app.mainloop()