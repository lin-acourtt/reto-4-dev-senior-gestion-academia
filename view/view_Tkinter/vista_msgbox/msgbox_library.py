from CTkMessagebox import CTkMessagebox
import customtkinter

def msg_registro_exitoso(tipo_entidad):
    """
        Ventana para indicar registro exitoso
    """
    CTkMessagebox(
                title= "Guardado",
                message= f"{tipo_entidad} registrado con éxito",
                icon= "check",
                option_1="OK"
            )

def msg_eliminacion_exitosa(tipo_entidad):
    """
        Ventana para indicar borrado exitoso
    """
    CTkMessagebox(
                title= "Borrado",
                message= f"{tipo_entidad} borrado con éxito",
                icon= "check",
                option_1="OK"
            )

def msg_sin_cambios():
    CTkMessagebox(
            title= "Sin cambios",
            message= "No se guardarán cambios",
            icon= "warning",
            option_1="OK"
        )
    
def msg_id_no_encontrado(id):
    CTkMessagebox(
            title= "No encontrado",
            message= f"No se encontró el ID {id}.",
            icon= "cancel",
            option_1="OK"
        )

def msg_error_campos_vacios():
    CTkMessagebox(
            title= "Error",
            message= f"Todos los campos son obligatorios.",
            icon= "cancel",
            option_1="OK"
        )

def msg_entrada_duplicada(tipo_entidad):
    CTkMessagebox(
            title= "Error",
            message= f"Ya existe un {tipo_entidad} con ese correo",
            icon= "cancel",
            option_1="OK"
        )

def msg_error_integrity(tipo_entidad, detalle):
    CTkMessagebox(
            title= "Error",
            message= f"Error al registrar {tipo_entidad}: {detalle}",
            icon= "cancel",
            option_1="OK"
        )

def msg_error_inesperado(detalle):
    CTkMessagebox(
            title= "Error",
            message= f"Error inesperado: {detalle}",
            icon= "cancel",
            option_1="OK")
    
def msg_no_hay_seleccion(tipo_entidad, accion):
    CTkMessagebox(
            title= "Error",
            message= f"Por favor, seleccione un {tipo_entidad} para {accion}.",
            icon= "warning",
            option_1="OK"
        )
    
def msg_hay_otra_ventana_abierta(tipo):
    CTkMessagebox(
            title= "Error",
            message= f"Ya hay una ventana de {tipo} abierta, por favor, cerrarla.",
            icon= "warning",
            option_1="OK"
        )

def msg_error_cargar_datos(tipo, mensaje):
    CTkMessagebox(
            title= "Error",
            message= f"Error al cargar datos de tipo '{tipo}'. Detalle: {mensaje}",
            icon= "warning",
            option_1="OK"
        )

################### Borrar
def show_info():
    # Default messagebox for showing some information
    CTkMessagebox(title="Info", message="This is a CTkMessagebox!")

def show_checkmark():
    # Show some positive message with the checkmark icon
    CTkMessagebox(message="CTkMessagebox is successfully installed.",
                  icon="check", option_1="Thanks")
    
def show_error():
    # Show some error message
    CTkMessagebox(title="Error", message="Something went wrong!!!", icon="cancel")
    
def show_warning():
    # Show some retry/cancel warnings
    msg = CTkMessagebox(title="Warning Message!", message="Unable to connect!",
                  icon="warning", option_1="Cancel", option_2="Retry")
    
    if msg.get()=="Retry":
        show_warning()
        
def ask_question():
    # get yes/no answers
    msg = CTkMessagebox(title="Exit?", message="Do you want to close the program?",
                        icon="question", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()
    
    if response=="Yes":
        app.destroy()       
    else:
        print("Click 'Yes' to exit!")
              
app = customtkinter.CTk()
app.rowconfigure((0,1,2,3,4,5), weight=1)
app.columnconfigure(0, weight=1)
app.minsize(200,250)

customtkinter.CTkLabel(app, text="CTk Messagebox Examples").grid(padx=20)
customtkinter.CTkButton(app, text="Check CTkMessagebox", command=show_checkmark).grid(padx=20, pady=10, sticky="news")
customtkinter.CTkButton(app, text="Show Info", command=show_info).grid(padx=20, pady=10, sticky="news")
customtkinter.CTkButton(app, text="Show Error", command=show_error).grid(padx=20, pady=10, sticky="news")
customtkinter.CTkButton(app, text="Show Warning", command=show_warning).grid(padx=20, pady=10, sticky="news")
customtkinter.CTkButton(app, text="Ask Question", command=ask_question).grid(padx=20, pady=(10,20), sticky="news")

#app.mainloop()