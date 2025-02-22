import sqlite3
import tkinter as tk
from tkinter import messagebox

def conectar_banco():
    conn = sqlite3.connect('farmacia.db')
    return conn

def criar_tabela():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicamentos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL,
                            descricao TEXT NOT NULL,
                            categoria TEXT NOT NULL
                        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

def adicionar_medicamento():
    nome = entry_nome.get()
    preco = float(entry_preco.get().replace(",", "."))
    descricao = entry_descricao.get()
    categoria = entry_categoria.get()
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Medicamentos (nome, preco, descricao, categoria)
                        VALUES (?, ?, ?, ?)''', (nome, preco, descricao, categoria))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Medicamento '{nome}' adicionado com sucesso.")
        limpar_campos()
        atualizar_listbox()  # Atualiza o Listbox depois de adicionar
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar medicamento: {e}")

def consultar_medicamento():
    id_medicamento = entry_id.get()
    
    if not id_medicamento.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
        return
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicamentos WHERE id = ?', (id_medicamento,))
        medicamento = cursor.fetchone()
        conn.close()

        if medicamento:
            detalhes = f"ID: {medicamento[0]}\nNome: {medicamento[1]}\nPreço: R${medicamento[2]:.2f}\nDescrição: {medicamento[3]}\nCategoria: {medicamento[4]}"
            messagebox.showinfo("Detalhes do Medicamento", detalhes)
        else:
            messagebox.showinfo("Consulta", "Medicamento não encontrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao consultar o medicamento: {e}")

def abrir_atualizar_medicamento():
    id_medicamento = entry_id.get()
    
    if not id_medicamento.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
        return
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicamentos WHERE id = ?', (id_medicamento,))
        medicamento = cursor.fetchone()
        conn.close()

        if medicamento:
            atualizar_janela(medicamento)
        else:
            messagebox.showinfo("Erro", "Medicamento não encontrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao consultar o medicamento: {e}")

def atualizar_janela(medicamento):
    atualizar_window = tk.Toplevel()
    atualizar_window.title("Atualizar Medicamento")

    tk.Label(atualizar_window, text="Nome do Medicamento").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(atualizar_window)
    nome_entry.insert(0, medicamento[1])
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(atualizar_window, text="Preço do Medicamento (R$)").grid(row=1, column=0, padx=10, pady=5)
    preco_entry = tk.Entry(atualizar_window)
    preco_entry.insert(0, f"{medicamento[2]:.2f}")
    preco_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(atualizar_window, text="Descrição do Medicamento").grid(row=2, column=0, padx=10, pady=5)
    descricao_entry = tk.Entry(atualizar_window)
    descricao_entry.insert(0, medicamento[3])
    descricao_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(atualizar_window, text="Categoria do Medicamento").grid(row=3, column=0, padx=10, pady=5)
    categoria_entry = tk.Entry(atualizar_window)
    categoria_entry.insert(0, medicamento[4])
    categoria_entry.grid(row=3, column=1, padx=10, pady=5)

    def salvar_atualizacao():
        novo_nome = nome_entry.get()
        novo_preco = float(preco_entry.get().replace(",", "."))
        nova_descricao = descricao_entry.get()
        nova_categoria = categoria_entry.get()

        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute('''UPDATE Medicamentos SET nome = ?, preco = ?, descricao = ?, categoria = ?
                              WHERE id = ?''', (novo_nome, novo_preco, nova_descricao, nova_categoria, medicamento[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Medicamento {novo_nome} atualizado com sucesso.")
            atualizar_listbox()  # Atualiza a lista após a atualização
            atualizar_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar medicamento: {e}")
    
    tk.Button(atualizar_window, text="Salvar Atualização", command=salvar_atualizacao).grid(row=4, column=0, columnspan=2, pady=10)

def atualizar_listbox():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicamentos')
        medicamentos = cursor.fetchall()
        conn.close()

        listbox.delete(0, tk.END)  # Limpa o Listbox antes de adicionar novos itens
        
        for medicamento in medicamentos:
            listbox.insert(tk.END, f"{medicamento[0]} - {medicamento[1]} - R${medicamento[2]:.2f}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar a lista de medicamentos: {e}")

def remover_medicamento():
    id_medicamento = entry_id.get()
    
    if not id_medicamento.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
        return
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicamentos WHERE id = ?', (id_medicamento,))
        medicamento = cursor.fetchone()

        if medicamento:
            cursor.execute('DELETE FROM Medicamentos WHERE id = ?', (id_medicamento,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Medicamento {medicamento[1]} removido com sucesso.")
            atualizar_listbox()  # Atualiza a lista após remoção
        else:
            messagebox.showinfo("Erro", "Medicamento não encontrado!")
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao remover o medicamento: {e}")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_id.delete(0, tk.END)

def criar_interface():
    global entry_nome, entry_preco, entry_descricao, entry_categoria, entry_id, listbox
    
    root = tk.Tk()
    root.title("Sistema de Gestão de Farmácia")
    
    tk.Label(root, text="Nome do Medicamento").grid(row=0, column=0, padx=10, pady=5)
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Preço do Medicamento (R$)").grid(row=1, column=0, padx=10, pady=5)
    entry_preco = tk.Entry(root)
    entry_preco.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Descrição do Medicamento").grid(row=2, column=0, padx=10, pady=5)
    entry_descricao = tk.Entry(root)
    entry_descricao.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Categoria do Medicamento").grid(row=3, column=0, padx=10, pady=5)
    entry_categoria = tk.Entry(root)
    entry_categoria.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Button(root, text="Adicionar Medicamento", command=adicionar_medicamento).grid(row=4, column=0, columnspan=2, pady=10)

    tk.Label(root, text="ID do Medicamento").grid(row=5, column=0, padx=10, pady=5)
    entry_id = tk.Entry(root)
    entry_id.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(root, text="Consultar Medicamento", command=consultar_medicamento).grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Atualizar Medicamento", command=abrir_atualizar_medicamento).grid(row=7, column=0, columnspan=2, pady=10)

    listbox = tk.Listbox(root, width=50, height=10)
    listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    tk.Button(root, text="Remover Medicamento", command=remover_medicamento).grid(row=9, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    criar_tabela()
    criar_interface()
    atualizar_listbox()
