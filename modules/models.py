import os
import sys
import time
import re
import json
import uuid
from inspect import currentframe
from keyboard import release, press
import pprint
from locale import setlocale, currency, LC_ALL

from pathlib import Path
from random import randint, choices
from datetime import datetime

class Autenticator:
    chaves_especiais = {
    "#": "a", "^": "b", "!": "c", "$": "d", "%": "e", "&": "f", "'": "g", "(": "h", ")": "i", "*": "j",
    "+": "k", ",": "l", "-": "m", ".": "n", "/": "o", ":": "p", ";": "q", "<": "r", "=": "s", ">": "t", "?": "u",
    "@": "v", "[": "w", "]": "x", "{": "y", "}": "z", "£": "3", "¢": "4", "¬": "5", "|": "6", "ª": "7", "º": "8", "§": "9",
    }

    chave_alf_car = {
        "a": "#", "b": "^", "c": "!", "d": "$", "e": "%", "f": "&", "g": "'", "h": "(", "i": ")",
        "j": "*", "k": "+", "l": ",", "m": "-", "n": ".", "o": "/", "p": ":", "q": ";", "r": "<", "s": "=", "t": ">", "u": "?",
        "v": "@", "w": "[", "x": "]", "y": "{", "z": "}", "3": "£", "4": "¢", "5": "¬", "6": "|", "7": "ª", "8": "º", "9": "§"
    }
    
    @classmethod
    def criptografar(cls, senha):
        senha_nova = ""
        for letra in senha:
            if letra in cls.chaves_especiais:
                senha_nova += cls.chaves_especiais[letra]
            else:
                try:
                    letra = letra.lower()
                except:
                    ...
                if letra in cls.chave_alf_car:
                    try:
                        senha_nova += cls.chave_alf_car[letra.lower()]
                    except:
                        senha_nova += cls.chave_alf_car[letra]
                else:
                    senha_nova += letra
        return senha_nova

    @classmethod
    def descriptografar(cls, senha_criptografada):
        senha_restaurada = ""
        for letra in senha_criptografada:
            if letra in cls.chaves_especiais:
                senha_restaurada += cls.chaves_especiais[letra]
            else:
                try:
                    senha_restaurada += cls.chave_alf_car[letra.lower()]
                except:
                    if letra in cls.chave_alf_car:
                        senha_restaurada += cls.chave_alf_car[letra]
                    else:
                        senha_restaurada += letra
        return senha_restaurada
    
    
    @staticmethod
    def validar_senha(senha):
        caracteres_especiais = ["!","@","#","$","%","¨¨","&","*","(",")","-","_","=","+","§","/","?",">","<",";",":"]

        if isinstance(senha, str): # Senha = Str
            if not ' ' in senha: # Senha não pode espaços
                contagem_caracte = 0
                contagem_num = 0
                for letra in senha: # Verifica se existe um caractere especial pelo menos
                    
                    if letra in caracteres_especiais:
                        contagem_caracte += 1
                        
                    try:
                        letra = int(letra)
                        contagem_num += 1
                    except Exception:
                        ...
                        
                    if contagem_num >= 2 and contagem_caracte >= 2:
                        if len(senha) > 7: # Senha deve ter mais que 7 caracteres
                                return True

        return False


    def auth_senha(self, senha="",conta=False):
        linha("Autenticador de Senha!")
        if not conta: # Vericação da existência da instância
            try:
                senha = self._senha
            except AttributeError:
                print('\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m')
        
        if not senha:
            tentativas = 3
            while not tentativas == 0: # Verificação do formato da senha
                senha = str(input('Digite a Senha: '))
                if ContaBancaria.validar_senha(senha):
                    break
                    
                if senha.startswith('Sair'):
                    return False
                
                tentativas -= 1
        else:
            if not ContaBancaria.validar_senha(senha):
                return False

        if conta: # Verificar a senha de uma conta especifica
            if ContaBancaria.contas[conta]['_senha'] == senha:
                return True
        elif self._senha == senha: # Verificando exatamente "minha senha"
            return True
        return False


class ContaBancaria(Autenticator):
    FILE = Path(__file__).parent / 'dados.json'
    taxa_juros = 1.01 # NUNCA, menor que 1.0

    contas = {}
    
    def __init__(self, num_conta="", ):
        linha("Iniciador de Contas!")
        
        antigo = None
        sair = False
        
        while True:
            try:
                # num_conta = int(input('Digite o número da conta [Conta nova/Antiga]: ')) # Validando!
                num_conta = 4
            except KeyboardInterrupt: # Opção para o usuário cancelar esse login, deixando claro que terá erros se usa essa instância,
            # pois não foi criada.
                print('\n\033[1;31mNão Use Essa Instância, Retornará ERR0!\033[m')
                print("Saindo da conta")
                sair = True
                break
            except Exception:
                print("\033[1;31m<<< Digite apenas números nessa entrada >>>\033[m")# Apenas para reiniciar o loop
            else:
                break
            
        if not sair: # Criando o cadastro, se quiser sair e ele pulará essa parte
            
            num_conta = str(num_conta)
            antigo = ContaBancaria.conta_existente(self,num_conta, senha="a12345@!")
            
            if antigo == "Conta nova" or not antigo:
                linha("Conta nova..")
                
                self._numero_conta = ContaBancaria.criar_num()
                print(f'Número de Conta atualizado: {self._numero_conta}')
                
                
                # Validação de Senha!
                # senha = str(input('Crie uma senha forte [Com 2 ou mais números e caracteres especiais]: '))
                senha = "a12345@!"
                while not ContaBancaria.validar_senha(senha):
                    senha = str(input('Digite a senha novamente: '))
                
                self._nome = ContaBancaria._validar_nome_completo(input("Nome completo: "))
                while self._nome == False:
                    self._nome = ContaBancaria._validar_nome_completo(input("Nome \033[1;31mcompleto\033[m: "))
                self._pix = {}
                self._saldo = 0
                self._senha = senha
                self._bloqueado = True
                self._divida_ativa = 0
                self._credito = False # Existência de um cartão de crédito
                self._registro = [{},{},{},{}]
                # {0} nome e valor gastado em um item no Crédito
                # {1} NOME E VALOR GASTADO EM UM ITEM DEBITO
                # {2} qual parcelas foram pagos e pagamento quitado 
                # {3} Faturas anteriores, passadas e futura (Virada de cartão dia 7)
            ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
            
    @property
    def numero_conta(self):
        return self._numero_conta
    
    def conta_existente(self,valor, senha=""):
        """Acessar e copiar dados já existente em outra conta antiga, trazendo para uma nova instância.

        Args:
            valor (str): Número da conta

        Returns:
            _type_: _description_
        """
        if ContaBancaria.buscar_por_numero(numero_conta=valor):
            if senha:
                if ContaBancaria.auth_senha(self, senha, conta=valor):
                    print(f"\033[1;33mConta acessado com sucesso!!\033[m\n")
                    ContaBancaria.copiar_conta(self,num=valor)
                    return True
                else:
                    print(f'\033[mVocê inseriu uma conta já existente, tente novamente com o número correto\033[m')
                    raise Exception("\033[1;31mVocê digitou a senha incorreta!\033[m")
            else:
                while True:
                    if ContaBancaria.auth_senha(self, conta=valor):
                        print(f"\033[1;33mConta acessado com sucesso!!\033[m\n")
                        ContaBancaria.copiar_conta(self,num=valor)
                        return True
                    else:
                        print(f'\033[mVocê inseriu uma conta já existente, tente novamente com o número correto\033[m')
                        return "Conta nova"
        else:
            self._numero_conta = valor
            return False

    @property
    def credito(self):
        return self._credito
    
    @credito.setter
    def credito(self, novo_valor_credito):
        if novo_valor_credito == True or novo_valor_credito == False:
            self._credito = novo_valor_credito
        else:
            print("Aceitamos apenas True/False")
    
    @property
    def pix(self):
        return self._pix
    
    @pix.setter
    def pix(self, nova_chave):
        self._pix = nova_chave

    @property
    def saldo(self):
        try:
            return self._saldo
        except AttributeError:
            print('\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m')
    
    @saldo.setter
    def saldo(self, novo_valor):
        try:
            self._saldo += novo_valor
        except AttributeError:
            print('\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m')
    
    
    @staticmethod
    def _validar_nome_completo(nome: str) -> bool:
        nome = nome.strip()

        # Verifica se tem pelo menos duas palavras
        partes = nome.split()
        if len(partes) < 2:
            return False

        # Regex para letras com acentos (nome válido)
        padrao = re.compile(r"^[A-Za-zÀ-ÿ]+$")

        for parte in partes:
            if not padrao.match(parte):
                return False

        return nome.title()

    
    
    @classmethod
    def criar_num(cls):
        alto = cls.contas.keys()
        if not alto:
            return 1
        return int(max(alto))+1
    
    @classmethod
    def buscar_por_numero(cls, numero_conta):
        if numero_conta in cls.contas:
            return cls.contas[numero_conta]
        return None
    
    def copiar_conta(self,num):
        try:
            self._numero_conta = num
            self._nome = ContaBancaria.contas[num]["_nome"]
            self._pix = ContaBancaria.contas[num]["_pix"]
            self._senha = ContaBancaria.contas[num]["_senha"]
            self._saldo = ContaBancaria.contas[num]["_saldo"]
            self._divida_ativa = ContaBancaria.contas[num]["_divida_ativa"]
            self._bloqueado = ContaBancaria.contas[num]["_bloqueado"]
            self._registro = ContaBancaria.contas[num]["_registro"]
            if "_limite" in ContaBancaria.contas[num]:
                self._limite = ContaBancaria.contas[num]["_limite"]
            self._credito = ContaBancaria.contas[num]["_credito"]
            if "_limite_atual" in ContaBancaria.contas[num]:
                self._limite_atual = ContaBancaria.contas[num]["_limite_atual"]
        except AttributeError:
            print('\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m')
    
    @staticmethod
    def loading_animation(mensagem="Carregando"):
        """
        Exibe uma animação de carregamento no console.
        
        Parâmetros:
        - style (str): Estilo da animação ('spinner' ou 'dots').
        
        Pressione Ctrl + C para interromper.
        """
        max_tempo = randint(5,30)
        tempo = 0
        count = 0
        print("\033[1;32m", end="")
        while True:
            count = (count + 1) % 4
            dots = '.' * count + ' ' * (7 - count)
            sys.stdout.write(f'\r{mensagem}{dots}')
            sys.stdout.flush()
            time.sleep(0.2)
            tempo += 1
            if tempo == max_tempo:
                break
        
        sys.stdout.write('\r' + ' ' * 30 + '\r')
        sys.stdout.flush()
        print("\033[m\r")
        
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _obter_data_atual():
        
        # Obtém a data e hora atuais
        data_atual = datetime.now()
        agora = datetime.now()
        
        # Extrai o dia, mês e ano
        dia = data_atual.day
        mes = data_atual.month
        ano = data_atual.year
        hora_atual = agora.strftime("%H:%M:%S")  # Formato 24h: HH:MM:SS

        
        
        return dia, mes, ano, hora_atual

    @staticmethod
    def _num_trans(texto):
        numero = ''
        for char in texto.split("_")[1]:
            if char.isdigit():
                numero += char
            else:
                break
        return int(numero)
    
    @staticmethod
    def _gerar_id():
        agora = datetime.now().strftime("%Y%m%d%H%M%S")  # e.g. 20250421123500
        aleatorio = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f"TX-{agora}-{aleatorio}"
    
    def bloquear_conta(self):
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({currentframe().f_code.co_name}) \033[m"\
        
        linha("Bloquear Conta!")
        
        if not ContaBancaria.auth_senha(self):
            return f'\033[1;31mBloqueio Negado!\033[m'
        
        self._bloqueado = True
        return f'\033[1;33mBloqueio Realizado com Sucesso\033[m'

    def desbloquear_conta(self, senha=""):
        
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({currentframe().f_code.co_name}) \033[m"
        
        linha("Desbloquear Conta!")
        
        if not ContaBancaria.auth_senha(self, senha):
            return f'\033[1;31mDesbloqueio Negado!\033[m'
        
        self._bloqueado = False
        return f'\033[1;33mDesbloqueio realizado com Sucesso!\033[m'

    def calcular_juros(self):
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({currentframe().f_code.co_name}) \033[m"\

        return self._saldo * ContaBancaria.taxa_juros

    @classmethod
    def atualizar_taxa_juros(cls,nova_taxa):
        cls.taxa_juros = nova_taxa

    @staticmethod
    def _numero_em_reais(numero):
        # Configura a localização para o Brasil
        setlocale(LC_ALL, 'pt_BR.UTF-8')
        # Formata como moeda (R$ 300.230,00)
        return currency(numero, symbol=True, grouping=True)

    @staticmethod
    def _formatar_numeros(*args):
        return float(round(*args, 2))
    
    def str_para_float(valor_str):
        # Remove o "R$", espaços e substitui vírgula por ponto
        valor_limpo = valor_str.replace("R$", "").strip().replace(".", "").replace(",", ".")
        return float(valor_limpo)

    def consultar_extrato(self): # > Testado!
        """
            Consultar extrato, não retorna nada, sem necessidade de chamar esse método pelo print
        """
        linha("Consultar Extrato!")
        
        lista_self = [self._registro[0],self._registro[1],self._registro[2]]
        conta = self.numero_conta
        if conta:
            lista_self = [ContaBancaria.contas[conta]['_registro'][0],ContaBancaria.contas[conta]['_registro'][1],\
                ContaBancaria.contas[conta]['_registro'][2]]
        
        print("\033[1;31mItens comprados no Crédito da conta:\033[m\n")
        # for item, valor in lista_self[0].items():
        #     print(f"{item} > R${valor}")
        p(lista_self[0], 2) # ! Atualizar para receber dicionário
        print("\033[1;31mItens comprados no Débito da conta:\033[m\n")
        p(lista_self[1], 2)
        print("\n\033[1;32mPagamentos realizados para quitar alguma dívida pendente:\033[m\n")
        p(lista_self[2], 2)
 
    @classmethod
    def _validar_conta(cls, conta_destino):
        """Verifica se a conta_destino é um número de conta ou chave PIX válida.
        
        Returns:
            tuple: (conta_encontrada: bool, numero_conta: str)
        """
        # Verifica se a conta_destino é um número de conta existente
        if conta_destino in cls.contas:
            return True, conta_destino, False
        
        for numero_conta, dados_conta in cls.contas.items():
            pix_info = dados_conta.get('_pix', {})
            for item, valor in pix_info.items():
                if conta_destino == valor:
                    return True, numero_conta, True
    
        # Se não encontrou
        return False, "", False

    def solicitar_cartao_credito(self): # > Testado!
        """Cartão de Crédito com limite de saldo do usuário no momento x 8

        Returns:
            str : Mensagem de Confirmação e Negado
        """
        linha("Solicitador de Cartão de Crédito!")
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        # Situações onde o cartão não será feito!
        if self._credito:
            return f"\033[1;33mEssa conta já possui cartão de crédito.\033[m"
        elif self._bloqueado:
            return f'\033[1;31mSolicitação Negada!\033[m\nMOTIVO: Conta Bloqueada'
        elif ContaBancaria.contas[self.numero_conta]["_saldo"] < 500: # Aqui é avaliado pelo saldo, mas é apresentar o score!
            return f'\033[1;31mCARTÃO NEGADO\033[m\nMOTIVO: Score abaixo da média'
        
        limite = self._saldo * 8
        self._limite = limite
        self._limite_atual = limite
        self._credito = True
        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        return  f'\033[1;33mSolicitação Aprovada\033[m\nCom limite de {self._limite}'
    
    def abrir_chave_pix(self, metodo=1, nova_chave=""):
        """Abrir chave pix

        Args:
            metodo (int, optional): 1 = PIX - CPF
                                    2 = PIX - Telefone
                                    3 = PIX - Email
                                    4 = Pix - Aleatória
            nova_chave (str, optional): _description_. Defaults to "".

        Returns:
            str: mensagem de confirmação ou erro
        """
        try: # Verificando a existência de instância
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        # Atualizando o dados salvo com o self atual
        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        

        tipos = ["1","2","3"]
        if not nova_chave:
            while True:
                try:
                    nova_chave = str(input('Digite sua nova chave pix [Telefone/Email/CPF - 4 = Aleatória]: '))
                    metodo = int(input('Digite o formato da chave[1 - CPF, 2 - Telefone, 3 - Email, 4 - Aleatória]: '))
                except Exception:
                    print(F'Digite a chave em string e formato em número - {Exception}')
                else:
                    break
        
        if not nova_chave in tipos:
            try:
                self._pix["pix_aleatoria"] = str(uuid.uuid4())
            except AttributeError:
                self._pix = {}
                self._pix["pix_aleatoria"] = str(uuid.uuid4())
            ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
            ContaBancaria.contas[self._numero_conta]["_pix"]["pix_aleatoria"] = str(uuid.uuid4())
            return "\033[1;33mNova chave pix ALEATÓRIA criada com sucesso!\033[m"
        
        if metodo == 1:
            if re.search(r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$", string=nova_chave):
                self._pix["pix_cpf"] = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"]["pix_cpf"] = nova_chave
                return "\033[1;33mNova chave pix CPF criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
        elif metodo == 2:
            if re.search(r"^(\+55)?\s?(\(?\d{2}\)?)?\s?9?\d{4}-?\d{4}$", string=nova_chave):
                self._pix["pix_fone"] = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"]["pix_fone"] = nova_chave
                return "\033[1;33mNova chave pix TELEFONE criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
        elif metodo == 3:
            if re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", string=nova_chave):
                self._pix['pix_email'] = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"]['pix_email'] = nova_chave
                return "\033[1;33mNova chave pix EMAIL criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
        

    def gerar_pdf(self, debito=False):
        # Atrasando importanção para evitar círculo de importação.
        from modules.pdf_gen import PDF 
        
        pdf = PDF()
        if debito:
            pdf.fatura(self._numero_conta, self._registro[1])
        else:
            pdf.fatura(self._numero_conta, self._registro[0])
        pdf.output("fatura.pdf")
        
    @staticmethod
    def limpar_terminal(fecha=False):
        
        """Limpa e fecha terminal

        Args:
            fecha (bool, optional): True fechará o terminal e assim terminado a execução do projeto
        """
        # Verifica o sistema operacional e executa o comando apropriado

        os.system('cls' if os.name == 'nt' else 'clear')
        if fecha:
            press('ctrl')  # Use 'ctrl' as a string for the Ctrl key
            press('1')
            release('ctrl')
            release('1')




def p(v,indent=2): 
    """ Print mais bonita, 
    mas não suporta várias coisas como sep, +-, etc..

    Args:
        v (_type_): Material/Conteúdo da Print
    """
    pprint.pprint(v, indent=indent)

def acessar_dados_antigos(numero_conta):
    """_summary_

    Args:
        numero_conta (str): numero_conta
    """
    a = ContaBancaria.buscar_por_numero(numero_conta)
    if not a:
        return print(f"\033[1;31mNão foi possível encontrada essa conta\033[m")
    entrada = ""
    while True:
        entrada = str(input('Digite o dado que deseja --> ')).lower()
        if entrada == 'sair':
            break
        if entrada == 'registro':
            try:
                tipo_lista = int(input('[0] - Compras Realizadas\n[1] - Movimentação do dinheiro dentro da conta\n[2] - Pagamentos da dívida com data.\nopção: '))
            except (TypeError, ValueError):
                print('\033[1;31mApenas números inteiros\033[m')
            p(a[entrada][tipo_lista])
        elif entrada == 'senha':
            print(f"Senha: {a["senha"]}")
        elif entrada == 'saldo':
            print(f"Saldo: R${a["saldo"]}")
        elif entrada == 'divida':
            print(f"Divida: \033[1;31m-R${a["divida_ativa"]}\033[m")
        elif entrada == "numero_conta":
            print(f'Número da conta: \033[4m{numero_conta}\033[m')
        elif entrada == "pix":
            print(f'Pix: {a['_pix']}')
        elif entrada == "bloqueado":
            print(f'Bloqueado: {a['bloqueado']}')
        elif entrada == "tudo":
            p(a)                
        else:
            print('\033[1;31mChave Inexistente\033[m')

def linha(mensagem):
    print("-" * len(mensagem))
    print(f"\033[1;32m{mensagem}\033[m")
    print("-" * len(mensagem))

def abreviar_mes(num_mes):
    if num_mes == 1:
        return "JAN"
    elif num_mes == 2:
        return "FEV"
    elif num_mes == 3:
        return "MAR"
    elif num_mes == 4:
        return "ABR"
    elif num_mes == 5:
        return "MAI"
    elif num_mes == 6:
        return "JUN"
    elif num_mes == 7:
        return "JUL"
    elif num_mes == 8:
        return "AGO"
    elif num_mes == 9:
        return "SET"
    elif num_mes == 10:
        return "OUT"
    elif num_mes == 11:
        return "NOV"
    elif num_mes == 12:
        return "DEZ"
    else:
        return "Número de mês inválido"
