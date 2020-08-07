from pyswip import Prolog
import tkinter
prolog = Prolog()
prolog.consult("file.pl")

# for value in prolog.query("shirt(X)"):
#     print(value["X"])

# create window object and give it a title
app = tkinter.Tk()
app.title('Smart House')

# resize default size
app.geometry('800x400')

# run app
app.mainloop()