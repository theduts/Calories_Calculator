import time
import os
import sqlite3

conexao = sqlite3.connect('alimentos.db')
cursor = conexao.cursor()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("===== Menu Contador de Calorias =====")
    print("1. Contar Calorias")
    print("2. Adicionar Itens")
    print("3. Remover Itens")
    # print("4. Ver itens")
    print("4. Consultar alimento")
    print("5. Sair")
    print("=====================================")

# def cadastro_VIA_SQL(item):
#     time.sleep(0.5)
#     clear_screen()
#     print('ADICIONAR ITEM\n')
    
#     cals = input(f'Calorias por 100g de {item}: ').strip()
    
#     cursor.execute('''INSERT INTO alimentos (Alimentos, Calorias) VALUES (?, ?)''', (item, cals))
#     conexao.commit()
    
#     print('Alimento cadastrado!')
#     time.sleep(2)

def cadastro_VIA_SQL(item):
    try:
        time.sleep(0.5)
        clear_screen()
        print('ADICIONAR ITEM\n')
        
        cals = input(f'Calorias por 100g de {item}: ').strip()
        
        cursor.execute('''INSERT INTO alimentos (Alimentos, Calorias) VALUES (?, ?)''', (item, cals))
        conexao.commit()
        
        print('Alimento cadastrado!')
        time.sleep(2)
    except sqlite3.OperationalError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        time.sleep(2)
        conexao.rollback()

def contar_VIA_SQL():
    calculo = []
    while True:
        time.sleep(0.5)
        clear_screen()
        print('CALCULADORA DE CALORIAS\n')
        item = input('Digite o alimento: (deixe vazio para terminar)').strip().capitalize()
        if item == '':
            break
        else:
            cursor.execute('SELECT * FROM alimentos WHERE Alimentos = ?', (item,)) #procura
            valores = cursor.fetchall() #e armazena o item se estiver no db
            
            if not valores: # Se o item não estive la dentro
                cadastrar = input(f'O item "{item}" não cadastrado. Deseja cadastrar? (s/n).')
                if cadastrar == 's':
                    cadastro_VIA_SQL(item)
                    # Reconsultar o banco de dados para obter o valor do item recém-cadastrado
                    cursor.execute('SELECT * FROM alimentos WHERE Alimentos = ?', (item,))
                    valores = cursor.fetchall()
                    
                    if valores:  # se encontrado
                        for alimento, caloria in valores:
                            calculo.append(int(caloria)) # Adiciona a caloria do item ao cálculo
                            print(f'Calorias adicionadas.')
                    
            else:
                for alimento, caloria in valores:
                    calculo.append(int(caloria))
                    print(f'Calorias adicionadas.')

    soma = sum(calculo)  # Usa a função sum() para somar os valores
    print(f'Ingestão calórica do dia: {soma:.2f} kcal')  # Formata a saída para duas casas decimais
    input('')

def adicionar_VIA_SQL():
    while True:
        time.sleep(0.5)
        clear_screen()
        print('ADICIONAR ITEM\n')
        item = input('Nome do Alimento ou refeição: (deixe vazio para sair)').strip().capitalize()
        if not item:
            break
        else:
            cursor.execute('SELECT * FROM alimentos WHERE Alimentos = ?', (item,)) #procura
            valores = cursor.fetchall() #e armazena o item se estiver no db
            
            if not valores: # Se o item não estive la dentro
                cadastro_VIA_SQL(item)
            else:
                print(f'{item} já cadastrado"')
                time.sleep(1)

def remover_VIA_SQL():
    time.sleep(0.5)
    clear_screen()
    print('Remoção de alimentos\n')
    
    item = input('Nome do alimento ou refeição a ser removido:').strip().capitalize()
    
    cursor.execute('DELETE FROM alimentos WHERE Alimentos = ?', (item,))
    conexao.commit()
    
    print('Alimento removido!')
    time.sleep(2)

# def ver_itens(itens):
#     clear_screen()
#     if not itens:
#         print('Não há itens na lista')
#     else:
#         for name, cals in itens.items():
#             print(f'{name}: {cals} (por 100g/ml)')
#     input('Pressione Enter para continuar...')

def consulta_VIA_SQL():
    while True:
        clear_screen()
        print('CONSULTA DE ITEM\n')
        item = input('Qual item deseja consultar? (deixe vazio para sair) ').strip().capitalize()
        if item == '':
            break
        else:
            cursor.execute(f'SELECT * FROM alimentos WHERE Alimentos="{item}"')
            valores = cursor.fetchall()
            
            # Verifica se o item foi encontrado
            if not valores:
                cadastrar = input(f'O item "{item}" não cadastrado. Deseja cadastrar? (s/n).')
                if cadastrar == 's':
                    cadastro_VIA_SQL(item)
            else:
                for alimento, caloria in valores:
                    print(f'{alimento}: {caloria} - 100g/ml')
            
            input('Pressione Enter para continuar...')

def main():
    #itens = alimentos
    while True:
        time.sleep(0.5)
        clear_screen()  # Limpa o output anterior antes de mostrar o menu
        mostrar_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            contar_VIA_SQL()
        elif escolha == '2':
            adicionar_VIA_SQL()
        elif escolha == '3':
            remover_VIA_SQL()
        # elif escolha == '4':
        #     ver_itens(itens)
        elif escolha == '4':
            consulta_VIA_SQL()
        elif escolha == '5':
            break
        else:
            time.sleep(0.5)
            clear_screen()  # Limpa o output anterior antes de mostrar o menu
            print('Selecione uma opção válida')
            time.sleep(2)

if __name__ == "__main__":
    main()

cursor.close()
conexao.close()