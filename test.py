"""import customtkinter as ctk
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime

class CalendarTest(ctk.CTk):

    def __init__(self):
        super().__init__()

    def iniciar(self):

        self.calendar = Calendar(self)    
        self.calendar.pack()

        self.date_entry = DateEntry(self,date_pattern='yyyy-MM-dd')    
        self.date_entry.pack()

        self.boton = ctk.CTkButton(
            self,
            text="Mostrar fecha",
            command=self.mostrar_fecha
        )
        self.boton.pack()

        self.boton2 = ctk.CTkButton(
            self,
            text="Setear fecha",
            command=self.setear_fecha
        )
        self.boton2.pack()

        self.mainloop()

    def mostrar_fecha(self):
        print(self.date_entry.get_date())

    def setear_fecha(self):

        date = '1994-03-17'
        date = datetime.strptime(date, "%Y-%m-%d")
            # This line will convert the datetime object to a date object
        date = datetime.date(date)
        self.date_entry.set_date(date)

test = CalendarTest()

test.iniciar()"""

hola='ID:374884'
print(hola[0:3])