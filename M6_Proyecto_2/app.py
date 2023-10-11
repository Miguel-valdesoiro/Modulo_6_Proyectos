import tkinter as tk
from tkinter import ttk, END, W, E
import sqlite3

class Producto:

    db = 'database/productos.db'

    def __init__(self, raiz):
        self.ventana = raiz
        self.ventana_editar = None
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        frame = ttk.LabelFrame(self.ventana, text="Registrar un nuevo Producto")
        frame.grid(row=1, column=0, columnspan=5, pady=5)

        self.etiqueta_nombre = ttk.Label(frame, text="Nombre:")
        self.etiqueta_nombre.grid(row=0, column=0)
        self.nombre = ttk.Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=0, column=1)

        self.etiqueta_categoria = ttk.Label(frame, text="Categoría:")
        self.etiqueta_categoria.grid(row=1, column=0)
        self.categoria = ttk.Entry(frame)
        self.categoria.grid(row=1, column=1)

        self.etiqueta_precio = ttk.Label(frame, text="Precio:")
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = ttk.Entry(frame)
        self.precio.grid(row=2, column=1)

        self.etiqueta_stock = ttk.Label(frame, text="Stock")
        self.etiqueta_stock.grid(row=3, column=0)
        self.stock = ttk.Entry(frame)
        self.stock.grid(row=3, column=1)

        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.app_producto)
        self.boton_aniadir.grid(row=4, columnspan=2, sticky=W + E)

        self.mensaje = tk.Label(text='', fg='red')
        self.mensaje.grid(row=2, column=0, columnspan=2, sticky=W + tk.E)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabla = ttk.Treeview(height=20, columns=("Nombre", "Categoría", "Precio", "Stock"),
                                  style="mystyle.Treeview")
        self.tabla.grid(row=3, column=0, columnspan=2, sticky='nswe')
        self.tabla.heading('#0', text='Nombre', anchor='center')
        self.tabla.heading('#1', text='Categoría', anchor='center')
        self.tabla.heading('#2', text='Precio', anchor='center')
        self.tabla.heading('#3', text='Stock', anchor='center')

        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto)
        boton_eliminar.grid(row=5, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto)
        boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            print(resultado)
            con.commit()
        return resultado

    def get_productos(self):
        registro_tabla = self.tabla.get_children()
        for fila in registro_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            print(fila)
            self.tabla.insert('', 0, text=fila[1], values=(fila[2], fila[3], fila[4]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_categoria(self):
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def validacion_stock(self):
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0

    def app_producto(self):
        if self.validacion_nombre() and self.validacion_categoria() and self.validacion_precio() and self.validacion_stock():
            nuevo_nombre = self.nombre.get()
            nueva_categoria = self.categoria.get()
            nuevo_precio = self.precio.get()
            nuevo_stock = self.stock.get()

            query = 'INSERT INTO producto VALUES(NULL, ?, ?, ?, ? )'
            parametros = (nuevo_nombre, nueva_categoria, nuevo_precio, nuevo_stock)
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(nuevo_nombre)
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.categoria.delete(0, END)
            self.precio.delete(0, END)  # Borrar el campo nombre del formulario
            self.stock.delete(0, END)
            self.get_productos()
        elif self.validacion_nombre() and self.validacion_categoria() and self.validacion_precio() and self.validacion_stock() == False:
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio'
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio'
        elif self.validacion_nombre() == False and self.validacion_categoria():
            print("La categoría es obligatoria")
            self.mensaje['text'] = 'La categoría es obligatoria'
        elif self.validacion_nombre() == False and self.validacion_categoria():
            print("La categoría es obligatoria")
            self.mensaje['text'] = 'el stock es obligatoria'
        else:
            print("El nombre, la categoría y el precio, el Stock son obligatorios")
            self.mensaje['text'] = 'El nombre, la categoría y el precio, el Stock  son obligatorios'

    def del_producto(self):
        self.mensaje['text'] = ''
        try:
            selected_item = self.tabla.selection()[0]
            nombre = self.tabla.item(selected_item)['text']
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            selected_item = self.tabla.selection()[0]
            nombre = self.tabla.item(selected_item)['text']
            old_categoria = self.tabla.item(selected_item)['values'][0]
            old_precio = self.tabla.item(selected_item)['values'][1]
            old_stock = self.tabla.item(selected_item)['values'][2]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.ventana_editar = tk.Toplevel()
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.geometry("600x550")
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')

        titulo = tk.Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0, columnspan=2)

        frame_ep = ttk.LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")
        frame_ep.grid(row=1, column=0, columnspan=2, pady=20)

        # Label Nombre antiguo
        label_nombre_anituguo = tk.Label(frame_ep, text="Nombre Antiguo:", font=("calibri", 13))
        label_nombre_anituguo.grid(row=0, column=0,)
        # Entry Nombre antiguo
        entry_nombre_anituguo = tk.Entry(frame_ep, textvariable=tk.StringVar(self.ventana_editar, value=nombre),state="readonly",font=("calibri", 13))
        entry_nombre_anituguo.grid(row=0, column=1, padx=10, pady=10)
        # Label Nombre nuevo
        label_nombre_nuevo = tk.Label(frame_ep, text="Nombre Nuevo:", font=("calibri", 13))
        label_nombre_nuevo.grid(row=1, column=0,)
        # Entry Nombre nuevo
        entry_nombre_nuevo = tk.Entry(frame_ep,)
        entry_nombre_nuevo.grid(row=1, column=1, padx=10, pady=10)
        #########
        # label Nombre antiguo
        label_categoria_antiguo = tk.Label(frame_ep, text="Categoría Antiguo:", font=("calibri", 13))
        label_categoria_antiguo.grid(row=2, column=0,)
        # entry Nombre antiguo
        entry_categoria_antiguo = tk.Entry(frame_ep, textvariable=tk.StringVar(self.ventana_editar, value=old_categoria),state="readonly",font=("calibri", 13))
        entry_categoria_antiguo.grid(row=2, column=1, padx=10, pady=10)
        # label Nombre nuevo
        label_categoria_nuevo = tk.Label(frame_ep, text="Categoría Nuevo:", font=("calibri", 13))
        label_categoria_nuevo.grid(row=3, column=0, )
        # Entry Nombre nuevo
        entry_categoria_nuevo = tk.Entry(frame_ep,)
        entry_categoria_nuevo.grid(row=3, column=1, padx=10, pady=10)
        ########
        # label Nombre antiguo
        label_precio_antiguo = tk.Label(frame_ep, text="Precio Antiguo:", font=("calibri", 13))
        label_precio_antiguo.grid(row=4, column=0,)
        # entry Nombre antiguo
        entry_precio_antiguo = tk.Entry(frame_ep, textvariable=tk.StringVar(self.ventana_editar,value=old_precio),state="readonly",font=("calibri", 13))
        entry_precio_antiguo.grid(row=4, column=1, padx=10, pady=10)
        # label Nombre nuevo
        label_precio_nuevo = tk.Label(frame_ep, text="Precio Nuevo:", font=("calibri", 13))
        label_precio_nuevo.grid(row=5, column=0,)
        # Entry Nombre nuevo
        entry_precio_nuevo = tk.Entry(frame_ep,)
        entry_precio_nuevo.grid(row=5, column=1, padx=10, pady=10)
        ########
        # label Nombre antiguo
        label_stock_antiguo = tk.Label(frame_ep, text="Stock Antiguo:", font=("calibri", 13))
        label_stock_antiguo.grid(row=6, column=0, )
        # Entry Nombre antiguo
        entry_stock_antiguo = tk.Entry(frame_ep, textvariable=tk.StringVar(self.ventana_editar,value=old_stock),state="readonly",font=("calibri", 13))
        entry_stock_antiguo.grid(row=6, column=1, padx=10, pady=10)
        # label Nombre nuevo
        label_stock_nuevo = tk.Label(frame_ep, text="Stock Nuevo:", font=("calibri", 13))
        label_stock_nuevo.grid(row=7, column=0,)
        # Entry Nombre nuevo
        entry_stock_nuevo = tk.Entry(frame_ep,)
        entry_stock_nuevo.grid(row=7, column=1, padx=10, pady=10)

        boton_guardar = tk.Button(
            frame_ep,
            text="Guardar Cambios",
            command=lambda: self.guardar_producto(
                self.nombre.get(),
                entry_nombre_nuevo.get(),
                self.categoria.get(),
                entry_categoria_nuevo.get(),
                self.precio.get(),
                entry_precio_nuevo.get(),
                self.stock.get(),
                entry_stock_nuevo.get()
            )
        )

        boton_guardar.grid(row=8, column=0, columnspan=2, pady=20, sticky=W + tk.E)

    def guardar_producto(self, nuevo_nombre, antiguo_nombre, nuevo_categoria, antiguo_categoria, nuevo_precio,
                         antiguo_precio, nuevo_stock, antiguo_stock):
        producto_modificado = False
        print(nuevo_nombre,nuevo_categoria,nuevo_precio,nuevo_stock)
        if (
                nuevo_nombre != antiguo_nombre
                or nuevo_categoria != antiguo_categoria
                or nuevo_precio != antiguo_precio
                or nuevo_stock != antiguo_stock
        ):
            producto_modificado = True

        query = "UPDATE producto SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE nombre = ? AND categoria = ? AND precio = ? AND stock = ?"

        parametros = (
            nuevo_nombre,
            nuevo_categoria,
            nuevo_precio,
            nuevo_stock,
            antiguo_nombre,
            antiguo_categoria,
            antiguo_precio,
            antiguo_stock,
        )

        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje["text"] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre)
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje["text"] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)


if __name__ == "__main__":
        root = tk.Tk()
        app = Producto(root)
        root.mainloop()


