import sqlite3
import tkinter as tk
from tkinter import messagebox

def conectar_banco():
    return sqlite3.connect('farmacia.db')

def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            descricao TEXT,
            categoria TEXT
        )
    ''')

    conn.commit()
    conn.close()

def adicionar_medicamento():
    nome = entry_nome.get()
    preco = entry_preco.get()
    descricao = entry_descricao.get()
    categoria = entry_categoria.get()

    if nome and preco and descricao and categoria:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Medicamentos (nome, preco, descricao, categoria)
            VALUES (?, ?, ?, ?)
        ''', (nome, float(preco), descricao, categoria))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Medicamento adicionado com sucesso!")
        limpar_campos()
        atualizar_lista()
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")

def consultar_medicamentos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Medicamentos')
    medicamentos = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)

    for medicamento in medicamentos:
        listbox.insert(tk.END, f"{medicamento[0]} - {medicamento[1]} - {medicamento[2]}")

def atualizar_medicamento():
    id_selecionado = listbox.curselection()
    if id_selecionado:
        id_medicamento = listbox.get(id_selecionado).split(" ")[0]
        nome = entry_nome.get()
        preco = entry_preco.get()
        descricao = entry_descricao.get()
        categoria = entry_categoria.get()

        if nome and preco and descricao and categoria:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Medicamentos
                SET nome = ?, preco = ?, descricao = ?, categoria = ?
                WHERE id = ?
            ''', (nome, float(preco), descricao, categoria, id_medicamento))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Medicamento atualizado com sucesso!")
            limpar_campos()
            atualizar_lista()
        else:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
    else:
        messagebox.showwarning("Erro", "Selecione um medicamento para atualizar!")

def remover_medicamento():
    id_selecionado = listbox.curselection()
    if id_selecionado:
        id_medicamento = listbox.get(id_selecionado).split(" ")[0]
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Medicamentos WHERE id = ?', (id_medicamento,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Medicamento removido com sucesso!")
        atualizar_lista()
    else:
        messagebox.showwarning("Erro", "Selecione um medicamento para remover!")

def atualizar_lista():
    listbox.delete(0, tk.END)
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Medicamentos')
    medicamentos = cursor.fetchall()
    conn.close()

    for medicamento in medicamentos:
        listbox.insert(tk.END, f"{medicamento[0]} - {medicamento[1]} - {medicamento[2]}")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)

root = tk.Tk()
root.title("Sistema de Gestão Farmacêutica")

tk.Label(root, text="Nome do Medicamento").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Preço").grid(row=1, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=1, column=1)

tk.Label(root, text="Descrição").grid(row=2, column=0)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=2, column=1)

tk.Label(root, text="Categoria").grid(row=3, column=0)
entry_categoria = tk.Entry(root)
entry_categoria.grid(row=3, column=1)

tk.Button(root, text="Adicionar Medicamento", command=adicionar_medicamento).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Consultar Medicamentos", command=consultar_medicamentos).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Atualizar Medicamento", command=atualizar_medicamento).grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Remover Medicamento", command=remover_medicamento).grid(row=7, column=0, columnspan=2)
tk.Button(root, text="Limpar Campos", command=limpar_campos).grid(row=8, column=0, columnspan=2)

listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=9, column=0, columnspan=2)

criar_tabelas()

root.mainloop()
