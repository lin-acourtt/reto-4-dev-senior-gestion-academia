# Aplicación de tkinter con el menú principal
from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
# Conexión a la base de datos
from config.database import Database

if __name__ == "__main__":
    # Objeto para conectar y hacer operaciones con la base de datos
    db = Database()
    try:
        # Crear la instancia del menú principal
        app = VentanaMenuPrincipal(db=db)
        # Iniciar el bucle principal de la aplicación
        app.iniciar_ventana()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
    finally:
        db.close()
