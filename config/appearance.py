import customtkinter as ctk

#### Windows' appearance
def centrar_ventana(ventana: ctk.CTk, proporcion=0.8):
    
    """Centra la venta respecto al tamaño de la pantalla"""

    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Asignar tamaño de la ventana, 80% del tamaño de la pantalla
    ancho_ventana = int(ancho_pantalla * proporcion)
    alto_ventana = int(alto_pantalla * proporcion)
    #ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

    # Coordenadas centradas
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")