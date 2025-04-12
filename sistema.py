# Atualizando e melhorando a classe feita no último exercício dessa pasta. 

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

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Configurações para o cabeçalho
        self.set_fill_color(70, 130, 180)  # Azul (Steel Blue)
        self.set_text_color(255, 255, 255)  # Branco para o texto do cabeçalho
        self.set_font("Arial", 'B', 14)
        # Cabeçalho com fundo colorido e centralizado
        self.cell(0, 12, 'Fatura de Compras', border=0, ln=1, align='C', fill=True)
        self.ln(4)  # Pequeno espaço após o cabeçalho
        self.set_text_color(0, 0, 0)  # Reseta a cor do texto para preto

    def footer(self):
        # Posiciona o rodapé a 15 unidades da borda inferior
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(128, 128, 128)  # Texto cinza
        # Número da página centralizado
        self.cell(0, 10, f'Página {self.page_no()}', border=0, ln=0, align='C')

    def fatura(self, numero_conta, registro):
        self.add_page()
        self.set_font("Arial", '', 12)

        # Título da fatura centralizado
        self.cell(0, 10, f"Fatura da conta: {numero_conta}", ln=True, align='C')
        self.ln(5)

        # Definição das larguras das colunas
        largura_item = 100
        largura_valor = 40
        table_width = largura_item + largura_valor

        # Calcula a posição para centralizar a tabela
        effective_width = self.w - self.l_margin - self.r_margin
        start_x = self.l_margin + (effective_width - table_width) / 2

        # Cabeçalho da tabela com preenchimento
        self.set_fill_color(200, 220, 255)  # Fundo azul claro para o cabeçalho
        self.set_text_color(0, 0, 0)
        self.set_draw_color(50, 50, 100)  # Cor para as bordas
        self.set_line_width(0.3)
        self.set_font("Arial", 'B', 12)

        # Define a posição inicial para o cabeçalho e imprime as células
        self.set_x(start_x)
        self.cell(largura_item, 10, 'Item', border=1, align='C', fill=True)
        self.cell(largura_valor, 10, 'Valores (R$)', border=1, align='C', fill=True)
        self.ln()

        # Dados da fatura com linhas alternadas para melhor visualização
        self.set_font("Arial", '', 12)
        fill = False  # Alterna o fundo das linhas
        for item, valor in registro.items():
            self.set_x(start_x)
            self.cell(largura_item, 10, item, border=1, align='L', fill=fill)
            self.cell(largura_valor, 10, f"{valor:.2f}", border=1, align='R', fill=fill)
            self.ln()
            fill = not fill  # Inverte o preenchimento para a próxima linha

        self.ln(5)

        # Linha de total destacada (também centralizada)
        total = sum(registro.values())
        self.set_x(start_x)
        self.set_font("Arial", 'B', 12)
        self.cell(largura_item, 10, 'Total', border=1)
        self.cell(largura_valor, 10, f"{total:.2f}", border=1, align='R')



class ContaBancaria(Autenticator):
    from pathlib import Path
    FILE = Path(__file__).parent / 'dados.json'
    taxa_juros = 1.09

    contas = {}
    
    def __init__(self, num_conta="", ):
        DataStorage.carregar()
        linha("Iniciador de Contas!")
        
        antigo = None
        sair = False
        
        while True:
            try:
                num_conta = int(input('Digite o número da conta [Conta nova/Antiga]: ')) # Validando!
            except KeyboardInterrupt: # Opção para o usuário cancelar esse login, deixando claro que terá erros se usa essa instância,
            # pois não foi criada.
                print('\n\033[1;31mNão Use Essa Instância, Retornará ERR0!\033[m')
                ContaBancaria.loading_animation("Saindo do Cadastro")
                sair = True
                break
            except Exception:
                print("\033[1;31m<<< Digite apenas números nessa entrada >>>\033[m")# Apenas para reiniciar o loop
            else:
                break
            
        if not sair: # Criando o cadastro, se quiser sair e ele pulará essa parte
            
            num_conta = str(num_conta)
            antigo = ContaBancaria.conta_existente(self,num_conta)
            
            if antigo == "Conta nova" or not antigo:
                
                while True: # Criando um número de conta aleátorio para não criar duas contas iguais 
                    from random import randint
                    num_conta = num_conta + str(randint(1000,10000))
                    if not ContaBancaria.buscar_por_numero(numero_conta=num_conta):
                        self._numero_conta = num_conta
                        break
                    
                print(f'Número de Conta atualizado: {num_conta}')
                self._pix = None # Abrindo Oportunidade de criação de chave pix
                senha = str(input('Crie uma senha forte [Com 2 ou mais números e caracteres especiais]: '))
                while not ContaBancaria.validar_senha(senha):
                    senha = str(input('Digite a senha novamente: '))
                self._senha = senha
                self._saldo = 0
                self._divida_ativa = 0
                self._bloqueado = True
                self._credito = False
                self._registro = [{},[],{}]
                # {0} nome e valor gastado em um item
                # {1} NOME E VALOR GASTADO EM UM ITEM DEBITO
                # {2} vezes que a divída foi pagar, sendo seguinte sintaxe: {pagamento_25_02_25: 24.0} 
            ContaBancaria.contas[num_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
            
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
                return "Conta nova"
            else:
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
    
    @classmethod
    def buscar_por_numero(cls, numero_conta):
        if numero_conta in cls.contas:
            return cls.contas[numero_conta]
        return None
    
    def copiar_conta(self,num):
        try:
            self._numero_conta = num
            self._pix = ContaBancaria.contas[num]["_pix"]
            self._senha = ContaBancaria.contas[num]["_senha"]
            self._saldo = ContaBancaria.contas[num]["_saldo"]
            self._divida_ativa = ContaBancaria.contas[num]["_divida_ativa"]
            self._bloqueado = ContaBancaria.contas[num]["_bloqueado"]
            self._registro = ContaBancaria.contas[num]["_registro"]
            self._credito = ContaBancaria.contas[num]["_credito"]
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
        import sys
        import time
        from random import randint
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
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _obter_data_atual():
        from datetime import datetime
        # Obtém a data e hora atuais
        data_atual = datetime.now()
        
        # Extrai o dia, mês e ano
        dia = data_atual.day
        mes = data_atual.month
        ano = data_atual.year
        
        return dia, mes, ano

    def bloquear_conta(self):
        import inspect
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({inspect.currentframe().f_code.co_name}) \033[m"\
        
        linha("Bloquear Conta!")
        
        if not ContaBancaria.auth_senha(self):
            return f'\033[1;31mBloqueio Negado!\033[m'
        
        self.bloqueado = True
        return f'\033[1;33mBloqueio Realizado com Sucesso\033[m'

    def desbloquear_conta(self):
        import inspect
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({inspect.currentframe().f_code.co_name}) \033[m"
        
        linha("Desbloquear Conta!")
        
        if not ContaBancaria.auth_senha(self):
            return f'\033[1;31mDesbloqueio Negado!\033[m'
        
        self._bloqueado = False
        return f'\033[1;33mDesbloqueio realizado com Sucesso!\033[m'

    def calcular_juros(self):
        import inspect
        # Verificando a existência de uma instância
        try:
            bloqueado = self._bloqueado
        except Exception:
            return f"\033[1;31mInstância Inexistente! ({inspect.currentframe().f_code.co_name}) \033[m"\

        return self.saldo * ContaBancaria.taxa_juros

    @classmethod
    def atualizar_taxa_juros(cls,nova_taxa):
        cls.taxa_juros = nova_taxa

    @staticmethod
    def _formatar_numeros(*args):
        return float(round(*args, 2))

    def quitar_divida(self, valor=0.0):
        linha("Quitar Dívida!")
        
        # Controle de Entradas
        
        if not valor:
            while True:
                try:
                    valor = float(input('O valor da parcela: '))
                except Exception:
                    return "\033[1;31mDigite apenas números (float)\033[m"
        else:
            try:
                valor = float(valor)
            except Exception:
                return "\033[1;31mDigite apenas números (float)\033[m"
        
        
        if self.divida_ativa == 0.0:
            return f'\033[1;32mNão se preocupe, você não tem nenhuma dívida.\033[m\nDívida: {self.divida_ativa}\n'
        elif valor > self.saldo:
            return '\033[1;31mSALDO INSUFICIENTE\033[m'


        if self.saldo < self.divida_ativa:
            if valor:
                data, mes, ano = ContaBancaria._obter_data_atual()
                self.divida_ativa -= valor # Pagar dívida
                self.saldo -= valor # Atualizar saldo
                self.registro[2][f'pagamento de {data} {mes} {ano}'] = valor
                self.registro[1].append(valor)
                return f'\033[1;31mDÍVIDA parcialmente QUITADA\033[m\nSALDO: {self.saldo}\nVALOR da Parcela: {valor}\n'\
                f'DÍVIDA: {self.divida_ativa}\n'
            else:
                self.divida_ativa -= self.saldo
                self.saldo = 0.0
                return f'\033[1;31mSua dívida NÃO FOI QUITADA completamente.\033[m\n'\
                    f'Saldo: \033[1;31m{self.saldo}\033[m\nDívida: \033[1;31m{self.divida_ativa}\033[m'

        self.saldo -= self.divida_ativa
        self.saldo = ContaBancaria._formatar_numeros(self.saldo)
        self.divida_ativa = ContaBancaria._formatar_numeros(self.divida_ativa)
        
        return f'Sua dívida foi quitada, seu saldo ficou: {self.saldo}'
    
    def consultar_extrato(self):
        """
            Consultar extrato, não retorna nada, sem necessidade de chamar esse método pelo print
        """
        linha("Consultar Extrato!")
        
        lista_self = [self._registro[0],self._registro[1],self._registro[2]]
        conta = self.numero_conta
        if conta:
            lista_self = [ContaBancaria.contas[conta]['_registro'][0],ContaBancaria.contas[conta]['_registro'][1],\
                ContaBancaria.contas[conta]['_registro'][2]]
        try:
            print("\033[1;31mItens gastos da conta:\033[m\n")
            p(lista_self[0], 2)
            print("\n\033[1;33mMovimentação do dinheiro na conta,\ncomo pagamentos, gastos e dinheiro enviado:\033[m\n")
            p(lista_self[1], 2)
            print("\n\033[1;32mPagamentos realizados para quitar alguma dívida pendente:\033[m\n")
            p(lista_self[2], 2)
        except Exception as erro:
            print(f"\033[1;4;31mOCORREU UM ERRO: {erro}")

    @classmethod
    def _validar_conta(cls, conta_destino):
        """Verifica se a conta_destino é um número de conta ou chave PIX válida.
        
        Returns:
            tuple: (conta_encontrada: bool, numero_conta: str)
        """
        # Verifica se a conta_destino é um número de conta existente
        if conta_destino in cls.contas:
            return True, conta_destino, False
        
        # Busca por chave PIX nas contas existentes
        for numero_conta, dados_conta in cls.contas.items():
            if dados_conta.get("_pix") == conta_destino:
                return True, numero_conta, True
        
        # Se não encontrou
        return False, "", False

    def solicitar_cartao_credito(self):
        """Cartão de Crédito com limite de saldo do usuário no momento x 8

        Returns:
            str : Mensagem de Confirmação e Negado
        """
        linha("Solicitador de Cartão de Crédito!")
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        if self.credito:
            return f"\033[1;33mEssa conta já possui cartão de crédito\033[m"
        
        if ContaBancaria.contas[self.numero_conta]["_saldo"] < 500:
            return f'\033[1;31mCARTÃO NEGADO\033[m\nMOTIVO: Saldo abaixo da média'
        
        if self._bloqueado:
            return f'\033[1;31mSolicitação Negada!\033[m\nMOTIVO: Conta Bloqueada'
        
        limite = self.saldo * 8
        self.limite = limite
        self._credito = True
        return  f'\033[1;33mSolicitação Aprovada\033[m\nCom limite de {self.limite}'
    
    def abrir_chave_pix(self, metodo=1, nova_chave=""):
        """Abrir chave pix

        Args:
            metodo (int, optional): 1 = PIX - CPF
                                    2 = PIX - Telefone
                                    3 = PIX - Email
            nova_chave (str, optional): _description_. Defaults to "".

        Returns:
            str: mensagem de confirmação ou erro
        """
        try: # Verificando a existência de instância
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        if not nova_chave:
            while True:
                try:
                    nova_chave = str(input('Digite sua nova chave pix [Telefone/Email/CPF]: '))
                    metodo = int(input('Digite o formato da chave[1 - CPF, 2 - Telefone, 3 - Email]: '))
                except Exception:
                    print('Digite a chave em string e formato em número')
                else:
                    break
            
        import re
        if metodo == 1:
            if re.search("^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$", string=nova_chave):
                self._pix = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"] = nova_chave
                return "\033[1;33mNova chave pix criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
        elif metodo == 2:
            if re.search("^(\+55)?\s?(\(?\d{2}\)?)?\s?9?\d{4}-?\d{4}$", string=nova_chave):
                self._pix = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"] = nova_chave
                return "\033[1;33mNova chave pix criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
        elif metodo == 3:
            if re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", string=nova_chave):
                self._pix = nova_chave
                ContaBancaria.contas[self.numero_conta]["_pix"] = nova_chave
                return "\033[1;33mNova chave pix criada com sucesso!\033[m"
            else:
                return "\033[1;31mChave pix com o formato incorreto!\033[m"
    
    def compra_com_credito(self, item="", valor_compra=0.0):
        """Compre com cartão de crédito, adiantando o pagamento do item

        Returns:
            Str: Mensagem de confirmação
        """
        linha("Pagamento com Crédito!")
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        if not self.credito:
            return f"\033[1;31mVocê não tem o cartão de crédito, tente usa o solicitar_cartao_credito\033[m"

        # Controle de Entradas
        if not item or not valor_compra:
            while True:
                try:
                    item = str(input("Digite o nome do item da compra: "))
                    valor_compra = float(input(f'Digite o valor de {item}: '))
                except Exception:
                    print('\033[1;31mDigite apenas texto na primeira entrada e float na segunda!\033[m')
                else:
                    break
        else:
            try:
                valor_compra = float(valor_compra)
                item = int(item) # Se o item vira inteiro, significa que só tem números aqui
                if not isinstance(item, str) and isinstance(valor_compra, float):
                    return "\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m"
            except Exception:
                print('\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m')
            
            
        self._registro[0][f'{item}'] = float(valor_compra)

        self._divida_ativa += valor_compra
        ContaBancaria.contas[self._numero_conta]["_divida_ativa"] += valor_compra
        
        return f'\033[1;33mCOMPRA EFETUADA COM SUCESSO\033[m\nItem: {item}\nValor: {valor_compra}\n'
    
    def compra_com_debito(self, item="", valor_compra=0.0):
        linha("Compra no Debito!")
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        # Controle de Entradas
        if not item or not valor_compra:
            while True:
                try:
                    item = str(input("Digite o nome do item da compra: "))
                    valor_compra = float(input(f'Digite o valor de {item}: '))
                except Exception:
                    ... # Apenas para reiniciar o loop
                else:
                    break
        else:
            try:
                valor_compra = float(valor_compra)
                if not isinstance(item, str) and not isinstance(valor_compra):
                    return "\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m"
            except Exception:
                return "\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m"
        
        self._registro[1][f'{item}'] = valor_compra
        
  
        ContaBancaria.contas[self.numero_conta]["_saldo"] -= valor_compra
        self.saldo -= ContaBancaria.contas[self.numero_conta]["_saldo"]
        
        return f'\033[1;33mCOMPRA EFETUADA COM SUCESSO\033[m\nItem: {item}\nValor: {valor_compra}\nSaldo Atual: {ContaBancaria.contas[self.numero_conta]["_saldo"]}'

    def gerar_pdf(self, debito=True):
        pdf = PDF()
        if debito:
            pdf.fatura(self._numero_conta, self._registro[1])
        else:
            pdf.fatura(self._numero_conta, self._registro[0])
        pdf.output("fatura.pdf")

class Transacao(ContaBancaria, Autenticator):
    def depositar(self, valor_depositar=0.0):
        linha("Depositar!")
        
        if not valor_depositar: # Tratando as duas formas de entrada por args e input
            while True:
                try:
                    valor_depositar = float(input('Digite o valor para depositar: '))
                except Exception:
                    print('\033[1;31mApenas float!\033[m')
                else:
                    break
        else:
            try:
                valor_depositar = float(valor_depositar)
            except Exception:
                return '\033[1;31mArg Incorreto, apenas float!\033[m'
            
        ContaBancaria.contas[self._numero_conta]["_saldo"] += valor_depositar

        return f"Saldo Atualizado: \033[1;33m{ContaBancaria.contas[self.numero_conta]["_saldo"]}\033[m"

    def transferir(self, conta_destino="", valor_de_transferencia=0.0):
        """Ao inserir um conta irá transferir o dinheiro para outra conta com uma taxa de 9%,
        ou se inserir a chave pix irá transferir o dinheiro para conta da pessoa sem taxa 

        Args:
            conta_destino (int): número do destinário
            valor_de_transferencia (float): Valor da transferência

        Returns:
            msg: Mensagens de retorno da situação do status de transferências
        """
        linha("Transferência!")
        
        # Controle de validação da Transferência
        if not conta_destino and valor_de_transferencia:
            try:
                valor_de_transferencia = float(valor_de_transferencia)
                if not isinstance(conta_destino, str) or not isinstance(valor_de_transferencia, float):
                    return f'\033[1;31mTipo Inválido, A conta_destino precisa se str e valor float\033[m'
            except:
                return f'\033[1;31mInfelizmente o "valor_de_transferencia" está com o tipo incorreto, tente novamente com float\033[m'
        else:
            while True:
                try:
                    conta_destino = str(input('Digite o número da conta destino: '))
                    conversao = int(conta_destino)
                    valor_de_transferencia = float(input('Digite o valor da transfêrencia: '))
                    print(f"Confirme seus dados.\nConta Destino: {conta_destino}\nValor da Transferência: {valor_de_transferencia}")
                    confirmar = str(input('Digite "S" para Confirmar ["N" para refazer]: ')).upper().startswith("S")
                except Exception:
                    print('Digite conta destino apenas com números inteiros, e valor em float')
                else:
                    if confirmar:
                        break
        
        
        conta_encontrada, num_conta, pix = ContaBancaria._validar_conta(conta_destino)
        print(conta_encontrada, num_conta)
        if not conta_encontrada:
            return '\033[1;31mConta inexistente\033[m'
        
        if not ContaBancaria.auth_senha(self):
            return f'\033[1;31mTransferência Negada\033[m\nMOTIVO: Senha incorreta!'
        
        if self.bloqueado:
            return f'\033[1;31mTransferência Negada\033[m\nMOTIVO: Conta Bloqueada!'
        
        if not self.saldo > valor_de_transferencia:
            return f'\033[1;31mSaldo Insuficiente\033[m'

        # Transferência Aprovada e sendo realizada
        ContaBancaria.contas[num_conta]['saldo'] += valor_de_transferencia 
        ContaBancaria.contas[num_conta]["registro"][1].append(valor_de_transferencia) # Registrando o ganho do usuário
          
        taxa = round(valor_de_transferencia * ContaBancaria.taxa_juros, 2) # Arredondamento a taxa
                
        if pix:
            self.saldo -= valor_de_transferencia # Via pix, é sem taxa.
            self.registro[1].append(-valor_de_transferencia)
            taxa = valor_de_transferencia
        else:
            self.saldo -= taxa
            self.registro[1].append(-taxa) 
        
        self.saldo = ContaBancaria._formatar_numeros(self.saldo)
        if f"Transferência_para_{conta_destino}" in self.registro[2]:
            self.registro[2][f"Transferência_para_{conta_destino}"] += taxa
        else:
            self.registro[2][f"Transferência_para_{conta_destino}"] = taxa
    
    
        # Duas mensagem diferente, a primeira sendo transferência padrão com taxa e a segunda e ultima com transferência
        # via pix
        return f'\033[1;33mTransferência Concluída\033[m com taxa\n'\
            f'Valor da Transferência: {valor_de_transferencia}\n'\
            f"\033[4;31mValor Extraído: {taxa}\033[m\n"\
            f'Seu Saldo Atual: {self.saldo}\n' \
            if not pix else \
            '\033[1;33mTransferência Concluída\033[m\n'\
            f'Valor da Transferência: {valor_de_transferencia}\n'\
            f'Valor Extraído: {valor_de_transferencia}\n'\
            f'Seu Saldo Atual: {self.saldo}\n'

    def sacar(self, valor_sacado=0.0):
        linha("Saque!")
       
        # Verificando possíveis problemas
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        if self._bloqueado:
            return f'\033[1;31mSaque Negado!\033[m\nMOTIVO: Conta Bloqueada'
        
        # Tratando ambas formas de entrada do método, por argumentos ou entrada input. 
        if not valor_sacado:
            while True:
                try:
                    valor_sacado = float(input(f'Digite o valor do saque: '))
                except Exception:
                    print('\033[mApenas número!\033[m')
                else:
                    break
        else:
            try:
                valor_sacado = float(valor_sacado)
            except Exception:
                return "\033[1;31m'valor_sacado' precisa se um número!\033[m"

        # Saque Aprovado, e sendo realizado e finalizado
        if not self.saldo >= valor_sacado:
            return f'\033[1;31mSaldo Insuficiente\033[m'
        
        self.saldo -= valor_sacado

        return f'\033[1;33mSaque Concluído\033[m\n'\
            f'Valor Sacado: {valor_sacado}\n'\
            f'Saldo Atual: {self.saldo}'

class DataStorage(ContaBancaria, Autenticator):
    @staticmethod
    def carregar(*, retorna_dado=False):
        ContaBancaria.loading_animation()
        
        import json
        
        try:
            with open(ContaBancaria.FILE, 'r', encoding='utf-8') as file_:
                dados = json.load(file_, )
            for item in dados:
                for itens in dados[item]:
                    if itens == "_senha":
                        dados[item]["_senha"] = Autenticator.descriptografar(dados[item]["_senha"])
            
            ContaBancaria.contas = dados  # Substitui a lista de contas
            return "\033[1;32mDados carregados com sucesso!\033[m"
        except FileNotFoundError:
            return "\033[1;31mArquivo não encontrado.\033[m"
        except Exception as e:
            return f"\033[1;31mErro ao carregar dados: {e}\033[m"
        
        if retorna_dado:
            return dados

    @classmethod
    def salvar(cls):
        ContaBancaria.loading_animation("Salvando")
        
        import json
        """
        Adiciona um novo dicionário a um arquivo JSON existente.

        Args:
            arquivo (str): Nome do arquivo JSON.
            novo valor (dict): Dicionário a ser adicionado.
        """
        for item in cls.contas:
            for itens in cls.contas[item]:
                if itens == "_senha":
                    cls.contas[item]["_senha"] = cls.criptografar(cls.contas[item]["_senha"])
        
        with open(cls.FILE, 'w', encoding='utf-8') as arquivo:
            json.dump(cls.contas, arquivo, indent=4, ensure_ascii=False)



def limpar_terminal(fecha=False):
    
    """Limpa e fecha terminal

    Args:
        fecha (bool, optional): True fechará o terminal e assim terminado a execução do projeto
    """
    # Verifica o sistema operacional e executa o comando apropriado
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    if fecha:
        import keyboard
        keyboard.press('ctrl')  # Use 'ctrl' as a string for the Ctrl key
        keyboard.press('1')
        keyboard.release('ctrl')
        keyboard.release('1')

def p(v,indent=2): 
    """ Print mais bonita, 
    mas não suporta várias coisas como sep, +-, etc..

    Args:
        v (_type_): Material/Conteúdo da Print
    """
    
    import pprint
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

# Criar uma conta bancária
a = Transacao()

# Criar uma instância de Transacao
# Depositar dinheiro na conta

print(a.compra_com_debito("Laser", 2))

# print(a.compra_com_debito("Mesa", 1200.00))
# print(a.compra_com_debito("Casa", 300000.00))  # casa é o único item com preço elevado justificado
# print(a.compra_com_debito("Cadeira", 350.50))
# print(a.compra_com_debito("Notebook", 4200.99))
# print(a.compra_com_debito("Smartphone", 2500.10))
# print(a.compra_com_debito("Geladeira", 3200.49))
# print(a.compra_com_debito("Fogão", 1700.00))
# print(a.compra_com_debito("Televisão", 2800.95))
# print(a.compra_com_debito("Sofá", 5200.00))
# print(a.compra_com_debito("Guarda-roupa", 3100.85))
# print(a.compra_com_debito("Cama", 2500.25))
# print(a.compra_com_debito("Bicicleta", 1700.99))
# print(a.compra_com_debito("Micro-ondas", 700.30))
# print(a.compra_com_debito("Impressora", 890.70))
# print(a.compra_com_debito("Aspirador de pó", 650.65))
# print(a.compra_com_debito("Máquina de lavar", 3700.40))

print(a.gerar_pdf())


# TODO: Menu de Lembrete!
sair = input("Deseja sair: ")
DataStorage.salvar()
limpar_terminal(True)
