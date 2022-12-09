import tkinter as tk
from cliente.gui_app import Frame,barra_menu


def main():
    ventana = tk.Tk()
    ventana.title("Catalogo de peliculas")
    ventana.iconbitmap("./img/peliculas.ico")
    ventana.resizable(0,0)
    barra_menu(ventana)


    app = Frame(ventana = ventana)
    
    app.mainloop()


if __name__ == "__main__":
    main()