from pyswip import Prolog
from tkinter import *
from tkinter import messagebox, ttk
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
    if dispInput.get() == '' or lugarDInput.get() == '' or tipoCombo.get() == '---Seleccione---':
        messagebox.showerror('Campos Requeridos','Debe introducir un dispositivo, su lugar y tipo en los campos.')
    else:
        if tipoCombo.get() == 'Otro':
            print(list(prolog.query("agregar_disp((%s, other), %s)" % (dispInput.get(), lugarDInput.get()))))
            resultado = list(prolog.query("lugar(%s,Tipo,Dispositivos)." % lugarDInput.get()))
            for ob in resultado:
                objetosLista.append(ob)
            clearInput()
            popularLista()
        elif tipoCombo.get() == 'Iluminacion':
            print(list(prolog.query("agregar_disp((%s, iluminacion), %s)" % (dispInput.get(), lugarDInput.get()))))
            resultado = list(prolog.query("lugar(%s,Tipo,Dispositivos)." % lugarDInput.get()))
            for ob in resultado:
                objetosLista.append(ob)
            clearInput()
            popularLista()
        elif tipoCombo.get() == 'Control de Temperatura':
            print(list(prolog.query("agregar_disp((%s, controlTemp), %s)" % (dispInput.get(), lugarDInput.get()))))
            resultado = list(prolog.query("lugar(%s,Tipo,Dispositivos)." % lugarDInput.get()))
            for ob in resultado:
                objetosLista.append(ob)
            clearInput()
            popularLista()
        elif tipoCombo.get() == 'Seguridad':
            print(list(prolog.query("agregar_disp((%s, seguridad), %s)" % (dispInput.get(), lugarDInput.get()))))
            resultado = list(prolog.query("lugar(%s,Tipo,Dispositivos)." % lugarDInput.get()))
            for ob in resultado:
                objetosLista.append(ob)
            clearInput()
            popularLista()

def eliminarDispositivo():
    if dispInput.get() == '' or lugarDInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un dispositivo y su respectivo lugar en los campos.')
    else:
        print(list(prolog.query("eliminar_disp(%s, %s)" % (dispInput.get(), lugarDInput.get()))))
        resultado = list(prolog.query("lugar(%s,Tipo,Dispositivos)." % lugarDInput.get()))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def agregarLugar():
    if lugarInput.get() == '' or tipoLCombo.get() == '---Seleccione---':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar y tipo en los campos.')
    else:
        print(list(prolog.query("agregar_lugar(%s, %s)" % (lugarInput.get(), tipoLCombo.get()))))
        resultado = list(prolog.query("lugar(Lugar,Tipo,Dispositivos)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def irLugar():
    if personaInput.get() == '' or lugarPInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir una persona y un lugar en los campos.')
    else:
        print(list(prolog.query("irLugar(%s, %s)" % (personaInput.get(), lugarPInput.get()))))
        resultado = list(prolog.query("ubicacion(Persona,Lugar)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def cambioLugar():
    if personaInput.get() == '' or lugarPInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir una persona y un lugar en los campos.')
    else:
        print(list(prolog.query("cambioLugar(%s, %s)" % (personaInput.get(), lugarPInput.get()))))
        resultado = list(prolog.query("ubicacion(Persona,Lugar)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def desactivarDispositivo():
    if dispDesactivarInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir una persona en el campo.')
    else:
        print(list(prolog.query("desactivar_dispositivos(%s)" % dispDesactivarInput.get())))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def desactivarTodos():
    if desactivarTodosInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar en el campo.')
    else:
        print(list(prolog.query("desactivarTodos(%s, X)" % desactivarTodosInput.get())))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def updateTemperature():
    if lugarTInput.get() == '' or temperaturaInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar y una temperatura en los campos.')
    else:
        print(list(prolog.query("actualizar_temperatura(%s, %s)" % (lugarTInput.get(), temperaturaInput.get()))))
        resultado = list(prolog.query("temperatura(Lugar, Temperatura)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def updateTime():
    if tiempoInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir una hora en el campo.')
    else:
        hora, minutos = tiempoInput.get().split(':')
        print(list(prolog.query("actualizar_tiempo(%s, %s)" % (hora, minutos))))
        resultado = list(prolog.query("tiempo(Hora, Minutos)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def getTemperature():
    resultado = list(prolog.query("temperatura(Lugar, Temperatura)."))
    for ob in resultado:
        objetosLista.append(ob)
    clearInput()
    popularLista()

def getTime():
    resultado = list(prolog.query("tiempo(Hora, Minutos)."))
    for ob in resultado:
        objetosLista.append(ob)
    clearInput()
    popularLista()

def encenderAC():
    if lugarACInput.get() == '' or tempACInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar y una temperatura en los campos.')
    else:
        print(list(prolog.query("encenderACManual(%s, %s)" % (lugarACInput.get(), tempACInput.get()))))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def apagarAC():
    if lugarACInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar en el campo.')
    else:
        print(list(prolog.query("apagarACManual(%s)" % lugarACInput.get())))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def encenderLuces():
    if lugarLucesInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar en el campo.')
    else:
        print(list(prolog.query("encenderLucesManual(%s)" % lugarLucesInput.get())))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def apagarLuces():
    if lugarLucesInput.get() == '':
        messagebox.showerror('Campos Requeridos','Debe introducir un lugar en el campo.')
    else:
        print(list(prolog.query("apagarLucesManual(%s)" % lugarLucesInput.get())))
        resultado = list(prolog.query("accion(Dispositivo, X, Estado)."))
        for ob in resultado:
            objetosLista.append(ob)
        clearInput()
        popularLista()

def dispEnUso():
    resultado = list(prolog.query("getDispositivosEnUso(Dispositivo, Estado, Descripcion)."))
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
    tipoLCombo.current(0)
    tipoCombo.current(0)
    estEntry.delete(0, END)
    lugarEntry.delete(0, END)
    lugarDEntry.delete(0, END)
    personaEntry.delete(0, END)
    lugarPEntry.delete(0, END)

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
app.geometry('1080x768')

# consult field and label
consultLabel = Label(app, text='Consulta General:', font=('bold', 14), bg="black", fg="white")
consultLabel.grid(row=0, column=0)
consultInput = StringVar()
consultEntry = Entry(app, textvariable=consultInput)
consultEntry.grid(row=0, column=1)

# consult button
consultBtn = Button(app, text='Consultar', command=realizarConsulta, pady=3)
consultBtn.grid(row=1, column = 0)

# agregar_lugar field and label
lugarLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
lugarLabel.grid(row=0, column=2)
lugarInput = StringVar()
lugarEntry = Entry(app, textvariable=lugarInput)
lugarEntry.grid(row=0, column=3)


tipoLCmbLabel = Label(app, text='Tipo(Lugar):', font=('bold', 14), bg="black", fg="white")
tipoLCmbLabel.grid(row=1, column=2)
tipoLCombo = ttk.Combobox(app, values=['---Seleccione---', 'sala', 'exterior', 'cocina', 'comedor', 'techo', 'entrada'])
tipoLCombo.current(0)
tipoLCombo.grid(row=1, column=3, padx=10)

# agregar_lugar button
lugarBtn = Button(app, text='Agregar Lugar', command=agregarLugar)
lugarBtn.grid(row=2, column = 2, pady=10)

# agregar_disp field and label
dispLabel = Label(app, text='Dispositivo:', font=('bold', 14), bg="black", fg="white")
dispLabel.grid(row=0, column=4)
dispInput = StringVar()
dispEntry = Entry(app, textvariable=dispInput)
dispEntry.grid(row=0, column=5)

lugarDLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
lugarDLabel.grid(row=1, column=4)
lugarDInput = StringVar()
lugarDEntry = Entry(app, textvariable=lugarDInput)
lugarDEntry.grid(row=1, column=5)

tipoCmbLabel = Label(app, text='Tipo(Disp):', font=('bold', 14), bg="black", fg="white")
tipoCmbLabel.grid(row=0, column=6)
tipoCombo = ttk.Combobox(app, values=['---Seleccione---', 'Iluminacion', 'Control de Temperatura', 'Seguridad', 'Otro'])
tipoCombo.current(0)
tipoCombo.grid(row=1, column=6, padx=10)


# agregar_disp button
dispBtn = Button(app, text='Agregar Dispositivo', command=agregarDispositivo)
dispBtn.grid(row=2, column = 4, pady=10)

# eliminar_disp button
elimDispBtn = Button(app, text='Eliminar Dispositivo', command=eliminarDispositivo)
elimDispBtn.grid(row=2, column = 5, pady=10)

# irLugar field and label
personaLabel = Label(app, text='Persona:', font=('bold', 14), bg="black", fg="white")
personaLabel.grid(row=3, column=0)
personaInput = StringVar()
personaEntry = Entry(app, textvariable=personaInput)
personaEntry.grid(row=3, column=1)

lugarPLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
lugarPLabel.grid(row=4, column=0)
lugarPInput = StringVar()
lugarPEntry = Entry(app, textvariable=lugarPInput)
lugarPEntry.grid(row=4, column=1)

# irLugar button
irLugarBtn = Button(app, text='Establecer Ubicacion', command=irLugar)
irLugarBtn.grid(row=5, column = 0, pady=10)

# cambioLugar button
cambioLugarBtn = Button(app, text='Actualizar Ubicacion', command=cambioLugar)
cambioLugarBtn.grid(row=5, column = 1, pady=10)

# desactivar_dispositivos field and label
dispDesactivarLabel = Label(app, text='Persona:', font=('bold', 14), bg="black", fg="white")
dispDesactivarLabel.grid(row=3, column=2)
dispDesactivarInput = StringVar()
dispDesactivarEntry = Entry(app, textvariable=dispDesactivarInput)
dispDesactivarEntry.grid(row=3, column=3)

# desactivar_dispositivos button
dispDesactivarBtn = Button(app, text='Desactivar dispositivo', command=desactivarDispositivo)
dispDesactivarBtn.grid(row=4, column = 2, pady=10)

# desactivar_todos field and label
desactivarTodosLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
desactivarTodosLabel.grid(row=3, column=4)
desactivarTodosInput = StringVar()
desactivarTodosEntry = Entry(app, textvariable=desactivarTodosInput)
desactivarTodosEntry.grid(row=3, column=5)

# desactivar_todos button
desactivarTodosBtn = Button(app, text='Desactivar disp. de lugar', command=desactivarTodos)
desactivarTodosBtn.grid(row=4, column = 4, pady=10)

# actualizar_temperatura field and label
lugarTLabel = Label(app, text='Lugar:', font=('bold', 14), bg="black", fg="white")
lugarTLabel.grid(row=6, column=0)
lugarTInput = StringVar()
lugarTEntry = Entry(app, textvariable=lugarTInput)
lugarTEntry.grid(row=6, column=1)

temperaturaLabel = Label(app, text='Temperatura:', font=('bold', 14), bg="black", fg="white")
temperaturaLabel.grid(row=7, column=0)
temperaturaInput = StringVar()
temperaturaEntry = Entry(app, textvariable=temperaturaInput)
temperaturaEntry.grid(row=7, column=1)

# actualizar_temperatura button
actualizarTempBtn = Button(app, text='Actualizar Temperatura', command=updateTemperature)
actualizarTempBtn.grid(row=8, column = 0, pady=10)

# getTempLugar button
getTempBtn = Button(app, text='Obtener Temperatura', command=getTemperature)
getTempBtn.grid(row=8, column = 1, pady=10)

# actualizar_tiempo field and label
tiempoLabel = Label(app, text='Hora:', font=('bold', 14), bg="black", fg="white")
tiempoLabel.grid(row=6, column=2)
tiempoInput = StringVar()
tiempoEntry = Entry(app, textvariable=tiempoInput)
tiempoEntry.grid(row=6, column=3)

# actualizar_tiempo button
actualizarTiempoBtn = Button(app, text='Actualizar Hora', command=updateTime)
actualizarTiempoBtn.grid(row=7, column = 2, pady=10)

# getTime button
getTimeBtn = Button(app, text='Obtener Hora', command=getTime)
getTimeBtn.grid(row=8, column = 2, pady=10)

# encenderACManual field and label
lugarACLabel = Label(app, text='Lugar(AC):', font=('bold', 14), bg="black", fg="white")
lugarACLabel.grid(row=6, column=4)
lugarACInput = StringVar()
lugarACEntry = Entry(app, textvariable=lugarACInput)
lugarACEntry.grid(row=6, column=5)

tempACLabel = Label(app, text='Temperatura(AC):', font=('bold', 14), bg="black", fg="white")
tempACLabel.grid(row=7, column=4)
tempACInput = StringVar()
tempACEntry = Entry(app, textvariable=tempACInput)
tempACEntry.grid(row=7, column=5)

# encenderACManual button
encenderACBtn = Button(app, text='Encender AC', command=encenderAC)
encenderACBtn.grid(row=8, column = 4, pady=10)

# apagarACManual button
apagarACBtn = Button(app, text='Apagar AC', command=apagarAC)
apagarACBtn.grid(row=8, column = 5, pady=10)

# encenderLucesManual field and label
lugarLucesLabel = Label(app, text='Lugar(luces):', font=('bold', 14), bg="black", fg="white")
lugarLucesLabel.grid(row=9, column=0)
lugarLucesInput = StringVar()
lugarLucesEntry = Entry(app, textvariable=lugarLucesInput)
lugarLucesEntry.grid(row=9, column=1)

# encenderLucesManual button
encenderLucesBtn = Button(app, text='Encender luces', command=encenderLuces)
encenderLucesBtn.grid(row=10, column = 0, pady=10)

# apagarLucesManual button
apagarLucesBtn = Button(app, text='Apagar luces', command=apagarLuces)
apagarLucesBtn.grid(row=10, column = 1, pady=10)

# getDispositivosEnUso button
dispEnUsoBtn = Button(app, text='Listar Dispositivos En Uso', command=dispEnUso)
dispEnUsoBtn.grid(row=9, column = 3, pady=10)

# list to show results
lista = Listbox(app, height=8, width=100, setgrid=0)
lista.grid(row=12, column=1, columnspan=6, rowspan=8, pady=25)

# Scrollbar for the list
scrollbar = Scrollbar(app)
scrollbar.grid(row=12, column=5, pady=25)

# Set scrollbar a la lista
lista.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=lista.yview)

# second window button
secondWinBtn = Button(app, text='Inputs y Sensores', command=secondWindow, pady=5)
secondWinBtn.grid(row=23, column = 3)

# ventana de bloquear sistema
ThirdWinBtn = Button(app, text="Bloquear Sistema", command=bloquearODesbloquear, pady=5)
ThirdWinBtn.grid(row=23, column = 4)

# estado de la casa  field and label
estLabel = Label(app, text='Estado de la casa:', font=('bold', 14), bg="black", fg="white")
estLabel.grid(row=26, column=1)
estInput = StringVar()
estEntry = Entry(app, textvariable=estInput)
estEntry.grid(row=26, column=2)

# agregar_estado casa button
fourthBtn = Button(app, text='Modificar estado', command=EstadoCasa)
fourthBtn.grid(row=26, column = 4)

fifthWinBtn = Button(app, text="Activar luces", command=luces, pady=5)
fifthWinBtn.grid(row=27, column = 4)

# run app
app.mainloop()