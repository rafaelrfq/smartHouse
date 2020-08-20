from pyswip import Prolog
from tkinter import *
from tkinter import messagebox
prolog = Prolog()
prolog.consult("smart_house.pl")

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
    contenido = Label(second, text='Aqui se pondra lo de insertar datos de sensores y eso').pack()

def bloquearODesbloquear():
    global stateOfTheHouse
    global ThirdWinBtn
    if stateOfTheHouse == 'Bloquear':
        stateOfTheHouse = 'Desbloquear'
        ThirdWinBtn.configure(text="bloquear Sistema")
        print(list(prolog.query("desbloquear.")))
        res = list(prolog.query("abertura(X), accion(X,Y)."))
        printListUnlock(res)
    else:
        stateOfTheHouse = 'Bloquear'
        ThirdWinBtn.configure(text="Desbloquear Sistema")
        print(list(prolog.query("bloquear.")))
        res = list(prolog.query("abertura(X), accion(X,Y)."))
        printListUnlock(res)

def printListUnlock(resultado):
    for ob in resultado:
        objetosLista.append(str(ob['X'] +':'+ob['Y']))
    clearInput()
    popularLista()

def EstadoCasa():
    if estInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un estado los campos')
    else:
        print(list(prolog.query("setEstadoCasa(%s)" % (estInput.get()))))
        resultado = list(prolog.query("verEstadoCasa(X)."))
        for ob in resultado:
            objetosLista.append(str('Estado: '+ ob['X']))
        clearInput()
        popularLista()

def luces():
    global fifthWinBtn
    state = list(prolog.query("verEstadoCasa(X)."))
    prolog.query("setLucesDelPatio.")
    if len(state) and state[0]['X'] == "noche":
        messagebox.showinfo('Exito','Las luces están prendidas')
    else:
        messagebox.showerror('Denegado','No se puede, el estado de la casa debe ser noche')

# create window object and give it a title
app = Tk()
app.title('Smart House')
app.iconbitmap('./house.ico')
stateOfTheHouse = 'Desbloquear'

# add background image
# C = Canvas(top, bg="blue", height=250, width=300)
bgimg = PhotoImage(file = "./background.png")
bg_label = Label(app, image=bgimg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# resize default size
app.geometry('960x540')

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
secondWinBtn = Button(app, text='Inputs y Sensores', command=secondWindow, pady=5)
secondWinBtn.grid(row=13, column = 3)

# ventana de bloquear sistema
ThirdWinBtn = Button(app, text="Bloquear Sistema", command=bloquearODesbloquear, pady=5)
ThirdWinBtn.grid(row=13, column = 4)

# estado de la casa  field and label
estLabel = Label(app, text='Estado de la casa:', font=('bold', 14), bg="black", fg="white")
estLabel.grid(row=16, column=1)
estInput = StringVar()
estEntry = Entry(app, textvariable=estInput)
estEntry.grid(row=16, column=2)

# agregar_estado casa button
fourthBtn = Button(app, text='Modificar estado', command=EstadoCasa)
fourthBtn.grid(row=16, column = 4)

fifthWinBtn = Button(app, text="Activar luces", command=luces, pady=5)
fifthWinBtn.grid(row=17, column = 4)

# run app
app.mainloop()