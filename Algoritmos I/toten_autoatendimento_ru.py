# Código do problema 01 do PBL de Algoritmos: ponto de autoatendimento do restaurante universitário da UEFS 
# Código desenvolvido único e exclusivamente por Gabriel Dantas Costa Carneiro sem utilização de ferramentas de inteligência artificial
# Aluno: Gabriel Dantas Costa Carneiro // Matrícula: 26111296
# Professora: Michele Fúlvia Angelo

# Variáveis e constantes globais de controle do sistema

student_counter = 0
professor_serv_counter = 0
visitant_counter = 0
stock_limit = 0
greater_change = 0
PASSWORD_ADMIN = '9999'
password_admin = ''

# Verificação de acesso do administrador para inicializar o sistema

while(password_admin != PASSWORD_ADMIN):

    password_admin = input('Digite a senha do administrador para iniciar o sistema:')

    if password_admin != PASSWORD_ADMIN:
        print('Senha inválida!')

print('\nBEM-VINDO, ADMINISTRADOR\n')

# Recebimento do valor do estoque para o dia

has_received_stock = False

while(not has_received_stock):

    stock_limit = input('Digite a quantidade de refeições do estoque de hoje (valor inteiro): ')

    if not stock_limit.isdigit():
        print('Digite um valor válido!') 
        
    else:

        if int(stock_limit) == 0:

            print('Digite um valor maior que zero!')

        else:
            has_received_stock = True
            stock_limit = int(stock_limit)
        

print('\nSISTEMA DE AUTOATENDIMENTO INICIADO COM SUCESSO!\n')
print(f'{stock_limit} refeições disponíveis para venda!')

# Menu de identificação de usuário

while(stock_limit > 0):

    category_value = 0
    category = 0
    has_received_value = False
    password_admin = ''

    print('\nBEM-VINDO AO CAIXA DE AUTOATENDIMENTO DA UEFS')
    print(f'TOTAL DE REFEIÇÕES RESTANTES: {stock_limit}\n')

    print('----------------------------------------')
    print('[1] - Aluno')
    print('[2] - Servidor/Professor')
    print('[3] - Visitante')
    print('[4] - Acesso Administrativo')
    print('---------------------------------------- \n')

    # Entrada de dados forçando a seleção de um usuário válido

    while(category != '1' and category != '2' and category != '3' and category != '4'):

        category = input('Digite o número correspondente a sua categoria:')

        if category != '1' and category != '2' and category != '3' and category != '4':
            print('Digite um valor válido!')

    # Tomada de decisão conforme índice escolhido

    if category == '1':

        register_number = ''

        while(not register_number.isdigit() or len(register_number) != 9):

            register_number = input('Digite seu número de matrícula: ')

            if not register_number.isdigit() or len(register_number) != 9: 
                print('Número de matrícula inválido! Deve conter apenas números e exatamente 9 dígitos.\n')

        category_value = 1.50
        print('\nOlá estudante! O valor do almoço é R$1,50')

    elif category == '2':
        category_value = 3.50
        print('\nOlá professor/servidor! O valor do almoço é R$3,50')

    elif category == '3':
        category_value = 12.00
        print('\nOlá visitante! O valor do almoço é R$12,00')

    else: 

        # Validação da senha de administrador para encerrar o sistema

        password_admin = input('Digite a senha de admnistrador para encerrar o sistema e visualizar o relatório do dia: ')

        if password_admin == PASSWORD_ADMIN:
            stock_limit = 0
            print('Sistema finalizado com sucesso!')

        else:
            print('Senha incorreta!')


    if category == '1' or category == '2' or category == '3':

        # Laço de tratamento de dados do recebimento do valor digitado para pagamento da refeição

        received_value = ''

        while(not has_received_value):

            received_value = input('Digite o valor que deseja utilizar para pagar o almoço: ')
            received_value = received_value.replace(',', '.')

            if not received_value.replace('.', '').isdigit() or received_value.count('.') > 1:
                print('Digite um valor válido!')
                
            else:
                has_received_value = True
            
        # Verificação do valor digitado e caso abaixo do necessário, solicita-se um novo valor para ser acrescentado

        change = float(received_value) - category_value

        if change < 0:
            
            print(f'Valor insuficiente! Faltam R${f'{abs(change):.2f}'.replace('.', ',')}')
            has_change_value = False

            while(not has_change_value):

                change_value = input('Digite o valor restante necessário ou a operação será cancelada: ')
                change_value = change_value.replace(',', '.')

                if not change_value.replace('.', '').isdigit() or change_value.count('.') > 1:
                    print('Digite um valor válido!')
                    
                else:
                    has_change_value = True
                    change += float(change_value)

        # Nova verificação do valor, caso inválido novamente, encerra o sistema, mas caso suficiente, adiciona o contador na respectiva categoria

        if change >= 0:

            # Adição do contador para a categoria utilizada e diminuição do estoque

            stock_limit -= 1

            if category == '1':
                student_counter += 1

            elif category == '2':
                professor_serv_counter += 1

            elif category == '3':
                visitant_counter += 1

            # Verificação do maior troco, atribuindo o valor se for maior que o anterior

            if change > greater_change:
                greater_change = change

            print(f'\nPagamento aprovado! Seu troco é de R${f'{change:.2f}'.replace('.', ',')}!')
            print('Volte sempre!')

        else:
            print(f'Pedido cancelado!')


# Finalização do sistema
# Verifica se o sistema foi finalizado pela sáida do administrador, caso tenha sido por falta de estoque (sem senha resgistrada), mostra a mensagem

if password_admin != PASSWORD_ADMIN:
    print('\nESTOQUE ZERADO!\n')

while(password_admin != PASSWORD_ADMIN):

    password_admin = input('Digite a senha de admnistrador para acessar o relarório do dia: ')

    if password_admin == PASSWORD_ADMIN:
        print('Sistema finalizado com sucesso!')

    else:
        print('Senha incorreta!')

# Processamento de dados do relatório

total_clients = student_counter + professor_serv_counter + visitant_counter
total_received_student = student_counter*1.50
total_received_professor_serv = professor_serv_counter*3.50
total_received_visitant = visitant_counter*12
total_collected = total_received_student + total_received_professor_serv + total_received_visitant
greater_value = 0
greater_category = ''

# Verificação de qual ou quais categorias foram as que mais arrecadaram valor

if total_received_student > total_received_professor_serv and total_received_student > total_received_visitant:
    greater_value = total_received_student
    greater_category = 'Os alunos foram a categoria com o maior valor'

elif total_received_student == total_received_professor_serv and total_received_student > total_received_visitant:
    greater_value = total_received_student
    greater_category = 'Os alunos e professores/servidores foram as categorias com o maior valor'

elif total_received_student == total_received_visitant and total_received_student > total_received_professor_serv:
    greater_value = total_received_student
    greater_category = 'Os alunos e visitantes foram as categorias com o maior valor'

elif total_received_professor_serv > total_received_student and total_received_professor_serv > total_received_visitant:
    greater_value = total_received_professor_serv
    greater_category = 'Os professores/servidores foram a categoria com o maior valor'

elif total_received_professor_serv == total_received_visitant and total_received_professor_serv > total_received_student:
    greater_value = total_received_professor_serv
    greater_category = 'Os professores/servidores e visitantes foram as categorias com o maior valor'

elif total_received_professor_serv == total_received_visitant and total_received_professor_serv == total_received_student:
    greater_value = total_received_professor_serv
    greater_category = 'Alunos, professores/servidores e visitantes tiveram valores iguais'

else:
    greater_value = total_received_visitant
    greater_category = 'Os visitantes foram a categoria com maior valor'

# Saída de dados do relatório
# Condicinal para evitar divisão por 0, caso relatório seja emitido sem refeições vendidas

if total_clients != 0:

    print('\nRELATÓRIO DO DIA!\n')
    print(f'Total de refeições vendidas: {total_clients}')
    print(f'Total refeições vendidas para alunos: {student_counter}')
    print(f'Total refeições vendidas para profgessores/servidores: {professor_serv_counter}')
    print(f'Total refeições vendidas para visitantes: {visitant_counter}')
    print(f'Total arrecadado: R${f'{total_collected:.2f}'.replace('.', ',')}')

    print(f'O ticket médio foi de: R${f'{(total_collected / total_clients):.2f}'.replace('.', ',')}\n')
    print(f'Alunos representaram {f'{((student_counter/total_clients) * 100):.1f}'.replace('.', ',')}% das refeições vendidas')
    print(f'Professores e servidores representaram {f'{((professor_serv_counter/total_clients) * 100):.1f}'.replace('.', ',')}% das refeições vendidas')
    print(f'Visitantes representaram {f'{((visitant_counter/total_clients) * 100):.1f}'.replace('.', ',')}% das refeições vendidas') 
    print(f'\n{greater_category} de vendas no RU hoje, com um total de R${f'{(greater_value):.2f}'.replace('.', ',')} em vendas')
    print(f'O maior troco devolvido foi de R${f'{(greater_change):.2f}'.replace('.', ',')}')

else:

    print(f'Não tiveram clientes hoje, portanto não teve relatório do dia!')
