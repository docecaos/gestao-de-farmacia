import sqlite3
import os
import platform

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
        print("Tabela criada ou já existe.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

def adicionar_medicamento():
    nome = input("Digite o nome do medicamento: ")
    preco_str = input("Digite o preço do medicamento: ")
    preco = float(preco_str.replace(",", "."))  # Substitui a vírgula por ponto
    descricao = input("Digite a descrição do medicamento: ")
    categoria = input("Digite a categoria do medicamento: ")
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Medicamentos (nome, preco, descricao, categoria)
                        VALUES (?, ?, ?, ?)''', (nome, preco, descricao, categoria))
        conn.commit()
        conn.close()
        print(f"Medicamento '{nome}' adicionado com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar medicamento: {e}")

def consultar_medicamentos():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Medicamentos')
        medicamentos = cursor.fetchall()
        conn.close()
        
        if medicamentos:
            print("Medicamentos cadastrados:")
            for medicamento in medicamentos:
                print(f"ID: {medicamento[0]} | Nome: {medicamento[1]} | Preço: R${medicamento[2]} | Descrição: {medicamento[3]} | Categoria: {medicamento[4]}")
        else:
            print("Nenhum medicamento encontrado.")
    except Exception as e:
        print(f"Erro ao consultar medicamentos: {e}")

def atualizar_medicamento():
    while True:
        id_medicamento_str = input("Digite o ID do medicamento a ser atualizado (ou 'sair' para cancelar): ")
        
        if id_medicamento_str.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if not id_medicamento_str:
            print("ID não pode ser vazio. Tente novamente.")
            continue
        
        try:
            id_medicamento = int(id_medicamento_str)
        except ValueError:
            print("ID inválido. Digite um número inteiro.")
            continue
        
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            
            # Consulta o medicamento atual para exibir os valores atuais
            cursor.execute('SELECT * FROM Medicamentos WHERE id = ?', (id_medicamento,))
            medicamento = cursor.fetchone()
            
            if medicamento:
                print(f"Medicamento atual: ID: {medicamento[0]} | Nome: {medicamento[1]} | Preço: R${medicamento[2]} | Descrição: {medicamento[3]} | Categoria: {medicamento[4]}")
                
                # Solicita os novos valores
                novo_nome = input("Digite o novo nome do medicamento (ou pressione Enter para manter o atual): ")
                novo_preco_str = input("Digite o novo preço do medicamento (ou pressione Enter para manter o atual): ")
                nova_descricao = input("Digite a nova descrição do medicamento (ou pressione Enter para manter a atual): ")
                nova_categoria = input("Digite a nova categoria do medicamento (ou pressione Enter para manter a atual): ")
                
                # Mantém os valores atuais se o usuário não fornecer novos valores
                novo_nome = novo_nome if novo_nome else medicamento[1]
                novo_preco = float(novo_preco_str.replace(",", ".")) if novo_preco_str else medicamento[2]
                nova_descricao = nova_descricao if nova_descricao else medicamento[3]
                nova_categoria = nova_categoria if nova_categoria else medicamento[4]
                
                # Atualiza o medicamento no banco de dados
                cursor.execute('''UPDATE Medicamentos 
                                SET nome = ?, preco = ?, descricao = ?, categoria = ? 
                                WHERE id = ?''', 
                              (novo_nome, novo_preco, nova_descricao, nova_categoria, id_medicamento))
                conn.commit()
                conn.close()
                print(f"Medicamento ID {id_medicamento} atualizado com sucesso.")
                break
            else:
                print(f"Medicamento com ID {id_medicamento} não encontrado.")
                break
        except Exception as e:
            print(f"Erro ao atualizar medicamento: {e}")
            break

def remover_medicamento():
    id_medicamento = int(input("Digite o ID do medicamento a ser removido: "))
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM Medicamentos WHERE id = ?''', (id_medicamento,))
        conn.commit()
        conn.close()
        print(f"Medicamento ID {id_medicamento} removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover medicamento: {e}")

def exibir_menu():
    while True:
        limpar_tela()
        print("\nSistema de Gestão de Farmácia")
        print("1. Adicionar Medicamento")
        print("2. Consultar Medicamentos")
        print("3. Atualizar Medicamento")
        print("4. Remover Medicamento")
        print("5. Sair")
        
        opcao = input("Escolha uma opção (1-5): ")
        
        if opcao == "1":
            adicionar_medicamento()
        elif opcao == "2":
            consultar_medicamentos()
        elif opcao == "3":
            atualizar_medicamento()
        elif opcao == "4":
            remover_medicamento()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione Enter para continuar...")

def limpar_tela():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():
    criar_tabela()
    exibir_menu()

if __name__ == "__main__":
    main()