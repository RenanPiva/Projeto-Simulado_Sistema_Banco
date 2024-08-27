from time import sleep
from datetime import datetime
import os
import sys

# Variaveis das Opções.

novoCliente = 1
delCliente = 2
debita = 3
deposita = 4
saldo = 5
extrato = 6
sair = 0

# Variaveis Globais Necessarias.

deletaCliente = ""
debitaCliente = ""
depositaCliente = ""
data_atual = datetime.today()
data_em_texto = "{}/{}/{} {}:{}".format(data_atual.day,
                                        data_atual.month,
                                        data_atual.year,
                                        data_atual.hour,
                                        data_atual.minute)


# Lista para usar de base para verificar se o usuario digitou uma opção valida em tipo de conta.

tipoContas = ['Comum', 'Salario', 'Plus', 'comum', 'salario', 'plus']

# Função que cadastra um novo cliente.

def nCliente():
    arq = open("cliente.txt", "a")
    
    nome = input("Digite o priemiro nome do novo cliente: ")
    cpf = input("Digite o CPF do novo cliente: ")
    tconta = input("Tipo de conta do cliente: \n (Salario) \n (Comum) \n (Plus) \n Digite: ")
    if tconta not in tipoContas:
        print(f'Não existe a opção {tconta}')
        return 'menu'
    valInicial = input("Digite o valor inicial da conta: ")
    senha = input("Digite a senha do usuario: ")

    carregamento()
    print ("Cliente Cadastrado com sucesso!")
    
    arq.write("\n%s %s %s %s %s " % (nome, cpf, tconta, valInicial, senha))
    arq.close()


# Função que apaga um cliente junto com o seu arquivo do extrato.

def dCliente():
    dCpf = str(input("Digite o cpf da conta que deseja deletar: "))
    
    t = 0
    
    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()
    
    for linha in checar:
        linhaS = linha.split(" ")
        for line in linhaS:
            
            if line == dCpf:
                deletaCliente = linhaS
                if os.path.isfile("extrato" + deletaCliente[0] + ".txt"):
                    os.remove("extrato" + deletaCliente[0] + ".txt")
                arq = open("cliente.txt", "w")
                t += 1
                for linha in checar:
                    linhaS = linha.split(" ")
                    if linhaS != deletaCliente:
                        arq.write(linha)
                
                carregamento()
                print("\nCliente deletado com sucesso.")
                arq.close()
                break
    
    if t == 0:
        print("CPF não encontrado.")


# Função que Debita.

def debitarC():
    debCpf = input("Digite o seu CPF: ")
    debSenha = input("Digite sua senha: ")
    debValor = float(input("Digite o valor a ser debitado: "))
    
    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()
    
    for linha in checar:
        linhaS = linha.split(" ")
        debitaCliente = linha.split(" ")
        if linhaS[0] == '\n':
                    continue
        if linhaS[1] == debCpf and linhaS[4] == debSenha:
            
            if linhaS[2] == "Salario" or linhaS[2] == "salario":
                debitaCliente[3] = float(debitaCliente[3])
                debitaCliente[3] = debitaCliente[3] - debValor * 1.05
                tarifa = debValor * 0.05
                
                if debitaCliente[3] < 0:
                    print("Debito não pertido.\n Seu saldo ficara abaixo de 0")
                    break
            
            elif linhaS[2] == "Comum" or linhaS[2] == "comum":
                debitaCliente[3] = float(debitaCliente[3])
                debitaCliente[3] = debitaCliente[3] - debValor * 1.03
                tarifa = debValor * 0.03
                
                if debitaCliente[3] < -500:
                    print("Debito não pertido.\n Seu saldo ficara abaixo de -500")
                    break
            
            elif linhaS[2] == "Plus" or linhaS[2] == 'plus':
                debitaCliente[3] = float(debitaCliente[3])
                debitaCliente[3] = debitaCliente[3] - debValor * 1.01
                tarifa = debValor * 0.01
            
                if debitaCliente[3] < -5000:
                    print("Debito não pertido.\n Seu saldo ficara abaixo de -5000")
                    break
                
            arq = open("cliente.txt", "w")
            
            i = 0
            
            for linha in checar:
                linhaS = linha.split(" ")
                if linhaS[0] == '\n':
                    continue
                if linhaS[1] == debitaCliente[1]:
                    for dbt in debitaCliente:
                        dbt = str(dbt)
                        
                        if i < 5:
                            i += 1
                            arq.write(dbt + " ")
                        
                        else:
                            arq.write(dbt)
                        
                        if i == 4:
                            extratoDeb = dbt
                            extratoDeb = float(extratoDeb)
                else:
                    arq.write(linha)
            arq.close()
            extrato1 = open("extrato" + debitaCliente[0] + ".txt", "a")
            extrato1.write("Data: %s - %.2f Tarifa: %.2f Saldo: %.2f\n" % (data_em_texto, debValor, tarifa, extratoDeb))
            extrato1.close()
            
            carregamento()
            print ("Debito Concluido com exito!")

            break


# Função que Deposita.

def depositoC():
    depCpf = input("Digite o seu CPF: ")
    depValor = float(input("Digite o valor a ser depositado: "))
    
    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()
    
    for linha in checar:
        linhaS = linha.split(" ")
        depositaCliente = linha.split(" ")
        if linhaS[0] == '\n':
            continue
        if depCpf == linhaS[1]:
            depositaCliente[3] = float(depositaCliente[3])
            depositaCliente[3] = depositaCliente[3] + depValor
            
            arq = open("cliente.txt", "w")
            
            i = 0
            
            for linha in checar:
                linhaS = linha.split(" ")
                if linhaS[0] == '\n':
                    continue
                if linhaS[1] == depositaCliente[1]:
                    for dbt in depositaCliente:
                        dbt = str(dbt)
                        
                        if i < 5:
                            i += 1
                            arq.write(dbt + " ")
                        
                        else:
                            arq.write(dbt)
                        
                        if i == 4:
                            extratoDep = dbt
                            extratoDep = float(extratoDep)
                else:
                    arq.write(linha)
            arq.close()
            
            extrato1 = open("extrato" + depositaCliente[0] + ".txt", "a")
            extrato1.write("Data: %s + %.2f Tarifa: 0.00 Saldo: %.2f\n" % (data_em_texto, depValor, extratoDep))
            extrato1.close()

            carregamento()
            print ("Deposito Concluido com exito!")

            break


# Função para verificar o saldo.

def saldoC():
    salCpf = input("Digite o seu CPF: ")
    salSenha = input("Digite sua senha: ")
    
    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()
    
    for linha in checar:
        linhaS = linha.split(" ")
        if linhaS[0] == '\n':
                    continue
        if linhaS[1] == salCpf and linhaS[4] == salSenha:
            print("\nSeu Saldo é de: " + linhaS[3])
            break


# Função para verificar o extrato.

def extratoC():
    exCpf = input("Digite o seu CPF: ")
    exSenha = input("Digite sua senha: ")
    
    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()
    
    for linha in checar:
        
        extratoCliente = linha.split(" ")
        if linha[0] == '\n':
                    continue
        if extratoCliente[1] == exCpf and extratoCliente[4] == exSenha:
            try:
                extrato1 = open("extrato" + extratoCliente[0] + ".txt",
                                "r")
                extratoArq = extrato1.readlines()
                extrato1.close()
                
                print("\nNome: %s" % extratoCliente[0])
                print("CPF: %s" % extratoCliente[1])
                print("Conta: %s\n" % extratoCliente[2])
                for linha in extratoArq:
                    print(linha, end=" ")
                
                break
            except: #TODO: except
                print("\nVocê ainda não realizou nenhum debito ou "
                      "deposito.")
                break


# Função que faz o efeito de carregamento do programa.

def carregamento():
    print(".")
    sleep(0.5)
    print("..")
    sleep(0.4)
    print("...")
    sleep(0.3)


# Função Menu que é responsavel por chamar todas as outras funções. 

def MeinMenu():
    print("Bem Vindo ao Banco QuemPoupaTem!")
    while True:
        print(
            "\n 1 - Cadastrar novo cliente \n"
            " 2 - Apaga Cliente \n"
            " 3 - Debita \n 4 - Deposita \n "
            "5 - Saldo \n 6 - Extrato \n\n 0 - Sair")

        opcao = int(input("\nEscolha uma opção: "))
        
        if opcao < 0 or opcao > 6:
            print("\nOpção invalida tente novamente.\n")
        
        else:
            if opcao == sair:
                print("Finalizando o sistema.")
                carregamento()
                break
            
            elif opcao == novoCliente:
                carregamento()
                valor = nCliente()
                if valor == 'menu':
                    continue
                else:
                    pass
            
            elif opcao == delCliente:
                carregamento()
                dCliente()
            
            elif opcao == debita:
                carregamento()
                debitarC()
            
            elif opcao == deposita:
                carregamento()
                depositoC()
            
            elif opcao == saldo:
                carregamento()
                saldoC()
            
            elif opcao == extrato:
                carregamento()
                extratoC()

MeinMenu()