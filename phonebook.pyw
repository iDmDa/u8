import sqlite3 as sq
from tkinter import *
from tkinter import ttk

def con():
    return sq.connect("telefon.db")

connect = con()
connect.execute("""create table if not exists ppl_list (
                        id integer primary key AUTOINCREMENT,
                        name text,
                        nomer text,
                        other text
                    )""")
connect.commit()

def tree_select(event):
    selection = tree.selection()
    if selection:
        item = tree.item(selection)
        id_entry.delete(0, END)
        id_entry.insert(END, item['values'][0])
        name_entry.delete(0, END)
        name_entry.insert(END, item['values'][1])
        telephone_entry.delete(0, END)
        telephone_entry.insert(END, item['values'][2])
        other_entry.delete(0, END)
        other_entry.insert(END, item['values'][3])

def save_data():
    connect = con()
    cursor = connect.cursor()
    cursor.execute(f"INSERT INTO ppl_list (name, nomer, other) VALUES ('{name_entry.get()}', '{telephone_entry.get()}', '{other_entry.get()}')")
    connect.commit()
    tree.delete(*tree.get_children())
    data = load_data()
    fill_widget(data)

def delete_data():
    connect = con()
    cursor = connect.cursor()
    cursor.execute(f"DELETE FROM ppl_list WHERE id = {id_entry.get()}")
    connect.commit()
    tree.delete(*tree.get_children())
    data = load_data()
    fill_widget(data)

def update_data():
    connect = con()
    cursor = connect.cursor()
    cursor.execute(f"UPDATE ppl_list SET name='{name_entry.get()}', nomer='{telephone_entry.get()}', other='{other_entry.get()}' WHERE id={id_entry.get()}")
    connect.commit()
    tree.delete(*tree.get_children())
    data = load_data()
    fill_widget(data)

def find_data():
    connect = con()
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM ppl_list WHERE name LIKE '%{find_entry.get()}%' or nomer LIKE '%{find_entry.get()}%' or other LIKE '%{find_entry.get()}%' ORDER BY name")
    connect.commit()
    tree.delete(*tree.get_children())
    data = cursor.fetchall()
    fill_widget(data)

def clear_entry():
    name_entry.delete(0, END)
    telephone_entry.delete(0, END)
    other_entry.delete(0, END)
    find_entry.delete(0, END)
    find_data()

def load_data():
    connect = con()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM ppl_list ORDER BY name')
    data = cursor.fetchall()
    connect.close()
    return data

def fill_widget(data):
    for item in data:
        tree.insert("", END, values=(item[0], item[1], item[2], item[3]))

window = Tk()  
window.title("Телефонный справочник")  
window.geometry('820x300')  
window.resizable(width=False, height=False)

tree = ttk.Treeview(columns=("id", "name", "nomer", "other"), show="headings")
tree.grid(row=0, column=0, columnspan=6, sticky="nsew")

tree.heading("id", text="id")
tree.heading("name", text="Имя")
tree.heading("nomer", text="Номер")
tree.heading("other", text="Примечание")

tree.column("id", width=0, stretch=False)

vsb = Scrollbar(window, orient="vertical", command=tree.yview)
vsb.place(x=800, y=10, height=210)
tree.configure(yscrollcommand=vsb.set)

id_entry = Entry(window, width=0)

Label(window, text="Найти:").grid(row=1, column=0)
find_entry = Entry(window, width=40)
find_entry.grid(row=1, column=1, columnspan=5, sticky="ew")

button_find = Button(window, text="Найти", command=find_data)
button_find.grid(row=1, column=5, columnspan=1, sticky="e")

Label(window, text="Имя:").grid(row=2, column=0)
name_entry = Entry(window, width=40)
name_entry.grid(row=2, column=1)

Label(window, text="Телефон:").grid(row=2, column=2)
telephone_entry = Entry(window, width=20)
telephone_entry.grid(row=2, column=3)

Label(window, text="Примечание:").grid(row=2, column=4)
other_entry = Entry(window, width=40)
other_entry.grid(row=2, column=5)

button_clear = Button(window, text="Очистить", command=clear_entry)
button_clear.grid(row=3, column=0, columnspan=1, sticky="ew")

button_add = Button(window, text="Добавить", command=save_data)
button_add.grid(row=3, column=1, columnspan=1, sticky="ew")

button_update = Button(window, text="Изменить", command=update_data)
button_update.grid(row=3, column=2, columnspan=1, sticky="ew")

button_delete = Button(window, text="Удалить", command=delete_data)
button_delete.grid(row=3, column=3, columnspan=1, sticky="ew")

data = load_data()

fill_widget(data)

tree.bind('<<TreeviewSelect>>', tree_select)

window.mainloop()