import customtkinter as ctk

#### Windows' appearance
def centrar_ventana(ventana: ctk.CTk, proporcion=0.8, *args):
    
    """
        Centra la venta respecto al tamaño de la pantalla

        Opciones de parámetros:
        - (a) -> solo proporcion horizontal
        - (proporcion=a) -> solo proporcion horizontal
        - (a,b) -> a: proporción horiztonal, b: proporcion vertical
    """

    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    if args:
        proporcion2 = args[0]
    else:
        proporcion2 = proporcion
    # Asignar tamaño de la ventana, 80% del tamaño de la pantalla
    ancho_ventana = int(ancho_pantalla * proporcion)
    alto_ventana = int(alto_pantalla * proporcion2)
    #ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

    # Coordenadas centradas
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")