import tkinter as tk
from tkinter import ttk
from model.pelicula_db import crear_tabla,eliminar_tabla
from model.pelicula_db import Pelicula,guardar,listar,editar,eliminar

from tkinter import messagebox

def barra_menu(ventana):
    barra_menu = tk.Menu(ventana)
    ventana.config(menu=barra_menu,width=300,height=300)
    menu_inicio = tk.Menu(barra_menu,tearoff=0)
    barra_menu.add_cascade(label="Inicio", menu=menu_inicio)

    menu_inicio.add_command(label="Crear registro en Base de Datos", command=crear_tabla)
    menu_inicio.add_command(label="Eliminar registro en Base de Datos", command=eliminar_tabla)
    menu_inicio.add_command(label="Salir",command=ventana.destroy)

    barra_menu.add_cascade(label="Consultas")
    barra_menu.add_cascade(label="Configuracion")
    barra_menu.add_cascade(label="Ayuda")

class Frame(tk.Frame):
    def __init__(self,ventana=None):
        super().__init__(ventana,width=480,height=320)
        self.ventana = ventana
        self.pack()
        #self.config(bg="gray")
        self.id_pelicula = None

        self.campos_peliculas()
        self.deshabilitar_campos()
        self.tabla_peliculas()
        

    def campos_peliculas(self):
        self.label_nombre = tk.Label(self,text = "Nombre: ")
        self.label_nombre.config(font=("Arial","12","bold"))
        self.label_nombre.grid(row=0,column=0,padx=10,pady=10)

        self.label_duracion = tk.Label(self,text = "Duracion: ")
        self.label_duracion.config(font=("Arial","12","bold"))
        self.label_duracion.grid(row=1,column=0,padx=10,pady=10)

        self.label_genero = tk.Label(self,text = "Genero: ")
        self.label_genero.config(font=("Arial","12","bold"))
        self.label_genero.grid(row=2,column=0,padx=10,pady=10)


        #entrys
        self.texto_nombre = tk.StringVar()

        self.entry_nombre = tk.Entry(self,textvariable=self.texto_nombre)
        self.entry_nombre.config(width=50,font=("Arial",12))
        self.entry_nombre.grid(row=0,column=1,padx=10,pady=10,columnspan=2)

        self.texto_duracion = tk.StringVar()

        self.entry_duracion = tk.Entry(self,textvariable=self.texto_duracion)
        self.entry_duracion.config(width=50,font=("Arial",12))
        self.entry_duracion.grid(row=1,column=1,padx=10,pady=10,columnspan=2)

        self.texto_genero = tk.StringVar()

        self.entry_genero = tk.Entry(self,textvariable=self.texto_genero)
        self.entry_genero.config(width=50,font=("Arial",12))
        self.entry_genero.grid(row=2,column=1,padx=10,pady=10,columnspan=2)


        #botones
        self.boton_nuevo = tk.Button(self,text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20,font=("Arial",12,"bold"),fg="#DAD5D6",bg="#239B56",cursor="hand2", activebackground="#82E0AA")
        self.boton_nuevo.grid(row=3,column=0,padx=10,pady=10)

        self.boton_guardar = tk.Button(self,text="Guardar", command=self.guardar_datos)
        self.boton_guardar.config(width=20,font=("Arial",12,"bold"),fg="#DAD5D6",bg="#2874A6",cursor="hand2", activebackground="#AED6F1")
        self.boton_guardar.grid(row=3,column=1,padx=10,pady=10)

        self.boton_cancelar = tk.Button(self,text="Cancelar",command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=20,font=("Arial",12,"bold"),fg="#DAD5D6",bg="#B03A2E",cursor="hand2", activebackground="#F5B7B1")
        self.boton_cancelar.grid(row=3,column=2,padx=10,pady=10)


    def habilitar_campos(self):
        self.texto_nombre.set("")
        self.texto_duracion.set("")
        self.texto_genero.set("")
        self.entry_nombre.config(state="normal")
        self.entry_duracion.config(state="normal")
        self.entry_genero.config(state="normal")

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def deshabilitar_campos(self):
        self.id_pelicula = None
        self.texto_nombre.set("")
        self.texto_duracion.set("")
        self.texto_genero.set("")
        self.entry_nombre.config(state="disabled")
        self.entry_duracion.config(state="disabled")
        self.entry_genero.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")
    
    def guardar_datos(self):
        pelicula = Pelicula(
            self.texto_nombre.get(),
            self.texto_duracion.get(),
            self.texto_genero.get()
        )

        if self.id_pelicula==None:
            guardar(pelicula)
        else:
            editar(pelicula,self.id_pelicula)


        self.tabla_peliculas()

        self.deshabilitar_campos()

    def tabla_peliculas(self):
        #recuperar la lista de peliculas
        self.lista_peliculas = listar()
        self.lista_peliculas.reverse()


        self.tabla = ttk.Treeview(self,column=("Nombre","Duracion","Genero"))
        self.tabla.grid(row=4,column=0,columnspan=4,sticky="nse")

        #scrollbar 
        self.scroll = ttk.Scrollbar(self,orient="vertical", command=self.tabla.yview)
        self.scroll.grid(row=4, column=4,sticky="nse")
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading("#0",text="ID")
        self.tabla.heading("#1",text="NOMBRE")
        self.tabla.heading("#2",text="DURACION")
        self.tabla.heading("#3",text="GENERO")


        #iterar la lista de peliculas
        for p in self.lista_peliculas:
            self.tabla.insert("",0,text=p[0],values=(p[1],p[2],p[3]))
    
        self.boton_modificar = tk.Button(self,text="Modificar" , command=self.edita_datos)
        self.boton_modificar.config(width=20,font=("Arial",12,"bold"),fg="#DAD5D6",bg="#239B56",cursor="hand2", activebackground="#82E0AA")
        self.boton_modificar.grid(row=5,column=0,padx=10,pady=10)

        self.boton_eliminar = tk.Button(self,text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(width=20,font=("Arial",12,"bold"),fg="#DAD5D6",bg="#B03A2E",cursor="hand2", activebackground="#F5B7B1")
        self.boton_eliminar.grid(row=5,column=1,padx=10,pady=10)

    def edita_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())["text"]
            self.nombre_pelicula = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.duracion_pelicula = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.genero_pelicula = self.tabla.item(
                self.tabla.selection())['values'][2]

            self.habilitar_campos()

            self.entry_nombre.insert(0,self.nombre_pelicula)
            self.entry_duracion.insert(0,self.duracion_pelicula)
            self.entry_genero.insert(0,self.genero_pelicula)
        except:
            titulo = "Edicion de datos"
            mensaje = "No ha seleccionado ningun registro"
            messagebox.showerror(titulo,mensaje)

    def eliminar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())["text"]
            eliminar(self.id_pelicula)
            self.tabla_peliculas()
            self.id_pelicula = None
        except:
            titulo = "Eliminar un Registro"
            mensaje = "No ha seleccionado ningun registro"
            messagebox.showerror(titulo,mensaje)