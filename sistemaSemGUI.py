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
                            categoria TEXT NOT NULL,
                            quantidade INTEGER NOT NULL
                        )''')
        conn.commit()
        conn.close()
        print("Tabela criada ou já existe.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

def adicionar_medicamento():
    nome = input("Digite o nome do medicamento: ")
    preco_str = input("Digite o preço do medicamento: ")
    preco = float(preco_str.replace(",", ".")) 
    descricao = input("Digite a descrição do medicamento: ")
    categoria = input("Digite a categoria do medicamento: ")
    quantidade = int(input("Digite a quantidade do medicamento: "))
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Medicamentos (nome, preco, descricao, categoria, quantidade)
                        VALUES (?, ?, ?, ?, ?)''', (nome, preco, descricao, categoria, quantidade))
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
                print(f"ID: {medicamento[0]} | Nome: {medicamento[1]} | Preço: R${medicamento[2]:.2f} | Descrição: {medicamento[3]} | Categoria: {medicamento[4]} | Quantidade: {medicamento[5]}")
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
                print(f"Medicamento atual: ID: {medicamento[0]} | Nome: {medicamento[1]} | Preço: R${medicamento[2]:.2f} | Descrição: {medicamento[3]} | Categoria: {medicamento[4]} | Quantidade: {medicamento[5]}")
                
                # Solicita os novos valores
                novo_nome = input("Digite o novo nome do medicamento (ou pressione Enter para manter o atual): ")
                novo_preco_str = input("Digite o novo preço do medicamento (ou pressione Enter para manter o atual): ")
                nova_descricao = input("Digite a nova descrição do medicamento (ou pressione Enter para manter a atual): ")
                nova_categoria = input("Digite a nova categoria do medicamento (ou pressione Enter para manter a atual): ")
                nova_quantidade_str = input("Digite a nova quantidade do medicamento (ou pressione Enter para manter a atual): ")
                
                # Mantém os valores atuais se o usuário não fornecer novos valores
                novo_nome = novo_nome if novo_nome else medicamento[1]
                novo_preco = float(novo_preco_str.replace(",", ".")) if novo_preco_str else medicamento[2]
                nova_descricao = nova_descricao if nova_descricao else medicamento[3]
                nova_categoria = nova_categoria if nova_categoria else medicamento[4]
                nova_quantidade = int(nova_quantidade_str) if nova_quantidade_str else medicamento[5]
                
                # Atualiza o medicamento no banco de dados
                cursor.execute('''UPDATE Medicamentos 
                                SET nome = ?, preco = ?, descricao = ?, categoria = ?, quantidade = ? 
                                WHERE id = ?''', 
                              (novo_nome, novo_preco, nova_descricao, nova_categoria, nova_quantidade, id_medicamento))
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

def vender_medicamento():
    carrinho = []
    while True:
        consultar_medicamentos()  # Mostra os medicamentos disponíveis
        id_medicamento = int(input("Digite o ID do medicamento a ser vendido: "))
        quantidade_vendida = int(input("Digite a quantidade a ser vendida: "))
        
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            
            # Verifica a quantidade disponível
            cursor.execute('SELECT quantidade, nome, preco FROM Medicamentos WHERE id = ?', (id_medicamento,))
            resultado = cursor.fetchone()
            
            if resultado:
                quantidade_atual, nome, preco = resultado
                if quantidade_atual >= quantidade_vendida:
                    carrinho.append({
                        'id': id_medicamento,
                        'nome': nome,
                        'quantidade': quantidade_vendida,
                        'preco': preco
                    })
                    print(f"Medicamento '{nome}' adicionado ao carrinho.")
                else:
                    print("Quantidade insuficiente em estoque.")
            else:
                print(f"Medicamento com ID {id_medicamento} não encontrado.")
            
            conn.close()
        except Exception as e:
            print(f"Erro ao verificar estoque: {e}")
        
        continuar = input("Deseja adicionar mais um medicamento ao carrinho? (s/n): ").strip().lower()
        if continuar != 's':
            break
    
    if carrinho:
        print("\nResumo da venda:")
        total_venda = 0
        for item in carrinho:
            subtotal = item['quantidade'] * item['preco']
            total_venda += subtotal
            print(f"{item['nome']} | Quantidade: {item['quantidade']} | Preço unitário: R${item['preco']:.2f} | Subtotal: R${subtotal:.2f}")
        print(f"Total da venda: R${total_venda:.2f}")
        
        confirmar = input("Confirmar venda? (s/n): ").strip().lower()
        if confirmar == 's':
            try:
                conn = conectar_banco()
                cursor = conn.cursor()
                for item in carrinho:
                    cursor.execute('UPDATE Medicamentos SET quantidade = quantidade - ? WHERE id = ?', 
                                   (item['quantidade'], item['id']))
                conn.commit()
                conn.close()
                print("Venda realizada com sucesso. Estoque atualizado.")
            except Exception as e:
                print(f"Erro ao atualizar estoque: {e}")
        else:
            print("Venda cancelada.")
    else:
        print("Nenhum medicamento no carrinho.")

def exibir_menu():
    while True:
        limpar_tela()
        print("\nSistema de Gestão de Farmácia")
        print("1. Adicionar Medicamento")
        print("2. Consultar Medicamentos")
        print("3. Atualizar Medicamento")
        print("4. Remover Medicamento")
        print("5. Vender Medicamento")
        print("6. Sair")
        
        opcao = input("Escolha uma opção (1-6): ")
        
        if opcao == "1":
            adicionar_medicamento()
        elif opcao == "2":
            consultar_medicamentos()
        elif opcao == "3":
            atualizar_medicamento()
        elif opcao == "4":
            remover_medicamento()
        elif opcao == "5":
            vender_medicamento()
        elif opcao == "6":
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