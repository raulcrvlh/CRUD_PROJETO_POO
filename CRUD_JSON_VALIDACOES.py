import json
import os
import re

class Cliente:
    def __init__(self, nome: str, idade: int, email: str) -> None:
        self.nome = nome
        self.idade = idade
        self.email = email

    def mostrar_cliente(self) -> dict:
        return {"Nome": self.nome, "Idade": self.idade, "E-mail": self.email}


class Sistema:
    def __init__(self) -> None:
        self.cadastro = {}
        self.carregar_dados()

    # validando dados
    def validar_nome(self):
        while True:
            nome = input("Digite o nome: ").upper().strip()
            verifica_nome = nome.replace(' ','')
            if len(nome) > 1 and verifica_nome.isalpha():  # Verifica se contém apenas letras
                return nome
            else:
                print("O nome deve conter apenas letras e não pode estar vazio.")

    def validar_idade(self):
        while True:
            idade = input("Digite a idade: ")
            try:
                if idade.isdigit():
                    idade = int(idade)
                    if 0 <= idade <= 100:  # Intervalo aceitável para idade
                        return idade
                    else:
                        print("A idade deve estar entre 0 e 100.")
                else:
                    print("Digite uma idade válida.")
            except ValueError:
                print("Por favor, insira um número válido para a idade.")

    def validar_email(self):
        while True:
            email = input("Digite o e-mail: ").strip()
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return email
            else:
                print("E-mail inválido. Tente novamente.")

    def validar_cpf(self):
        while True:
            cpf = input("Digite o CPF do cliente: ")
            cpf = cpf.strip().replace('.', '').replace('-', '')
            if len(cpf) != 11:
                return ("O CPF deve conter 11 digitos numéricos.")
            else:
                return cpf

    # Função para salvar dados no arquivo cadastros.json
    def salvar_dados(self, arquivo="cadastros.json"):
        try:
            with open(arquivo, "w") as f:
                json.dump({cpf: cliente.__dict__ for cpf, cliente in self.cadastro.items()}, f, indent=4)
            print("Dados salvos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    # Função para carregar dados do arquivo cadastros.json
    def carregar_dados(self, arquivo="cadastros.json"):
        try:
            if os.path.exists(arquivo):
                with open(arquivo, "r") as f:
                    conteudo = f.read().strip()
                    if conteudo:
                        dados = json.loads(conteudo)
                        self.cadastro = {cpf: Cliente(**cliente) for cpf, cliente in dados.items()}
                        print("Dados carregados com sucesso.")
                    else:
                        print("Arquivo JSON vazio.")
        except FileNotFoundError:
            print("Arquivo não encontrado. Um novo será criado.")
        except json.JSONDecodeError:
            print("Erro no formato do arquivo JSON.")

    def verificar_existencia(self, cpf: str) -> bool:
        if cpf not in self.cadastro:
            print(f"O cliente com CPF {cpf} não foi encontrado.")
            return False
        return True

    # Função para criar um novo cliente
    def create(self, cpf: str):
        if cpf in self.cadastro:
            print(f"O cliente com CPF {cpf} já está cadastrado.")
            return
        nome = self.validar_nome()
        idade = self.validar_idade()
        email = self.validar_email()
        self.cadastro[cpf] = Cliente(nome, idade, email)
        self.salvar_dados()
        print(f"Cliente com CPF {cpf} cadastrado com sucesso!")

    # Função para imprimir os clientes cadastrados
    def read(self):
        if not self.cadastro:
            print("Nenhum cliente cadastrado.")
        else:
            for cpf, cliente in self.cadastro.items():
                print(f"CPF: {cpf}")
                info_cliente = cliente.mostrar_cliente()
                for key, value in info_cliente.items():
                    print(f"{key}: {value}")
                print("-" * 20)
    
     # Função para alterar dados de um cliente
    def update(self, cpf: str):
        if cpf in self.cadastro:
            cliente = self.cadastro[cpf]
            print("Deixe em branco se não quiser alterar o campo.")
            nome = input(f"Digite o novo nome do cliente (atual: {cliente.nome}): ").upper()
            if nome:
                cliente.nome = nome

            idade = input(f"Digite a nova idade do cliente (atual: {cliente.idade}): ")
            if idade:
                cliente.idade = int(idade)

            email = input(f"Digite o novo e-mail do cliente (atual: {cliente.email}): ")
            if email:
                cliente.email = email

            self.salvar_dados()  # Salva todos os dados no arquivo após a atualização
            print(f"Cadastro do cliente com CPF {cpf} alterado com sucesso!")
        else:
            print("Cliente não encontrado.")

    # Função para deletar um cliente do cadastro
    def delete(self, cpf: str):
        if cpf in self.cadastro:
            if self.confirmar_exclusao(cpf):
                self.cadastro.pop(cpf)
                self.salvar_dados()
                print(f"O cliente com CPF {cpf} foi deletado com sucesso.")
        else:
            print("Cliente não encontrado.")
        
    def confirmar_exclusao(self, cpf: str):
        confirmacao = input(f"Tem certeza que deseja excluir o cliente com CPF {cpf}? (S/N): ").lower()
        return confirmacao == 's'
    
    # Função para sair do sistema
    def exit(self) -> bool:
        print("Saindo do sistema. Até logo!")
        return True

    # Menu principal
    def menu(self):
        while True:
            try:
                print('-' * 40)
                print("| Escolha uma opção:                   |")
                print("| 1. Cadastrar novo cliente            |")
                print("| 2. Alterar cadastro existente        |")
                print("| 3. Imprimir clientes cadastrados     |")
                print("| 4. Deletar um cadastro.              |")
                print("| 5. Sair                              |")
                print('-' * 40)

                opcao = input("Opção: ")

                if opcao == "1":
                    # cpf = input("Digite o CPF do cliente: ").strip()
                    cpf = self.validar_cpf()
                    self.create(cpf)

                elif opcao == "2":
                    cpf = self.validar_cpf()
                    if self.verificar_existencia(cpf):
                        self.update(cpf)

                elif opcao == "3":
                    self.read()

                elif opcao == "4":
                    cpf = self.validar_cpf()
                    self.delete(cpf)

                elif opcao == "5":
                    if self.exit():
                        break

                else:
                    print("Opção inválida. Tente novamente.")

            except Exception as e:
                print(f"Ocorreu um erro: {e}")

sistema = Sistema()
sistema.menu()
