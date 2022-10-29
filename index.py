from cProfile import label
from cgitb import text
from sre_parse import State
from tkinter import ttk
from tkinter import *

import sqlite3
from tkinter.tix import COLUMN
from unicodedata import name
from unittest import TestCase


class Product:
    # connection dir property
    db_name = 'database.db'
    

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Products Application')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Register new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        #price input
        Label(frame, text='Price:').grid(row=2, column= 0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #button agregar producto
        ttk.Button(frame, text='Guardar', command = self.add_product).grid(row=3, columnspan=2, sticky= W + E)

        #auput messager

        self.message = Label(text='', fg = 'red' )
        self.message.grid(row = 3, column= 0, columnspan= 2, sticky= W + E)

        #Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text='Name', anchor = CENTER)
        self.tree.heading('#1', text='Precio', anchor = CENTER)

        ttk.Button(text= 'ELIMINAR', command = self.delete_product ).grid(row = 5, column= 0, sticky= W + E)
        ttk.Button(text= 'EDIT', command=self.edit_product ).grid(row = 5, column= 1, sticky= W + E)

        self.get_product()

    def run_query(self, query, parameters = () ):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def get_product(self):

        #eliminar
        record = self.tree.get_children()
        for elemento in record:
            self.tree.delete(elemento)
        #consultando
        query ='SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text= row[1], values=row[2])


    def validation(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0


    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ? )'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'el producto esta guardado' + self.name.get()
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:    
            self.message['text'] = 'El nombre y el precio son requeridos'
        self.get_product()

    def delete_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un Registro'
            return
        name = self.tree.item(self.tree.selection())['text']    
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Eliminado' + self.name.get()
        self.get_product()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un Registro'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_vent = Toplevel()
        self.edit_vent.title = 'Edit product'

        Label(self.edit_vent, text='OLd Name').grid(row=0, column= 1)
        Entry(self.edit_vent, textvariable= StringVar(self.edit_vent, value= name), state = 'readonly').grid(row=0, column=2 )

        Label(self.edit_vent, text = 'New Name').grid(row = 1, column = 1)
        new_name = Entry(self.edit_vent)
        new_name.grid(row= 1, column=2)

        Label(self.edit_vent, text='OLd price').grid(row=2, column= 1)
        Entry(self.edit_vent, textvariable= StringVar(self.edit_vent, value= old_price), state = 'readonly').grid(row=2, column=2 )

        Label(self.edit_vent, text = 'New Price').grid(row = 3, column = 1)
        new_Precio = Entry(self.edit_vent)
        new_Precio.grid(row= 3, column=2)


        Button(self.edit_vent, text= 'Update', command = lambda: self.edit_record(new_name.get(), name, new_Precio.get(), old_price )).grid(row = 4, column= 2 , sticky= W +E)

    def edit_record(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, precio = ? WHERE name = ? AND precio = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_vent.destroy()
        self.message['text'] = 'Acutalizado'
        self.get_product()



if __name__ == '__main__':
 window = Tk()
 application = Product(window)
 window.mainloop()
