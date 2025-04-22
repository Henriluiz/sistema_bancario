from modules.models import ContaBancaria, Autenticator, linha, datetime, choices
class Transacao(ContaBancaria):
    def __init__(self):
        super().__init__()
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
        

        self._saldo += valor_depositar

        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        return f"Saldo Atualizado: \033[1;33m{self._saldo}\033[m"

    @staticmethod
    def _buscado_por_transferir(mensagem_transferencia):
        texto = f"Transferência 123.456789 para conta_destino no 01 Janeiro 2024"

        # Padrão regex para capturar o número (inteiro ou decimal)
        padrao = r"Transferência\s+(\d+\.\d+|\d+)"

        # Busca pelo padrão no texto
        match = re.search(padrao, texto)

        if match:
            numero = int(match.group(1))  # Converte para float
            return numero
        else:
            return False

    def transferir(self, conta_destino="", valor_de_transferencia=0.0):
        """Ao inserir um conta irá transferir o dinheiro para outra conta com uma taxa de 9%,
        ou se inserir a chave pix irá transferir o dinheiro para conta da pessoa sem taxa 

        Args:
            conta_destino (int): número do destinário
            valor_de_transferencia (float): Valor da transferência

        Returns:
            msg: Mensagens de retorno da situação do status de transferências
        """
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
        def _gerar_id_transacao():
            agora = datetime.now().strftime("%Y%m%d%H%M%S")  # e.g. 20250421123500
            aleatorio = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            return f"TX-{agora}-{aleatorio}"
        linha("Transferência!")
        
        # Controle de validação da Transferência
        if conta_destino and valor_de_transferencia:
            try:
                valor_de_transferencia = float(valor_de_transferencia)
                if not isinstance(conta_destino, str) or not isinstance(valor_de_transferencia, float):
                    return f'\033[1;31mTipo Inválido, A conta_destino precisa se str e valor float\033[m'
            except:
                return f'\033[1;31mInfelizmente o "valor_de_transferencia" está com o tipo incorreto, tente novamente com float\033[m'
        else:
            while True:
                try:
                    conta_destino = input('Digite o número da conta destino: ')
                    converso = int(conta_destino)
                    
                    valor_de_transferencia = float(input('Digite o valor da transfêrencia: '))
                    print(f"Confirme seus dados.\nConta Destino: {conta_destino}\nValor da Transferência: {valor_de_transferencia}")
                    confirmar = input('Digite "S" para Confirmar ["N" para refazer]: ').upper().startswith("S")
                    
                except Exception:
                    print('Digite conta destino apenas com números inteiros, e valor em float')
                else:
                    if confirmar:
                        break
        
        
        conta_encontrada, num_conta, pix = ContaBancaria._validar_conta(conta_destino)
        
        if not conta_encontrada:
            return '\033[1;31mConta inexistente\033[m'
        
        if not ContaBancaria.auth_senha(self):
            return f'\033[1;31mTransferência Negada\033[m\nMOTIVO: Senha incorreta!'
        
        if self._bloqueado:
            return f'\033[1;31mTransferência Negada\033[m\nMOTIVO: Conta Bloqueada!'
        
        if valor_de_transferencia > self._saldo:
            return f'\033[1;31mSaldo Insuficiente\033[m'

        if self._numero_conta == conta_destino:
            return f'\033[1;31mImpossível realizar uma transação para sua própria conta, use depositar() para essa ação\033[m'

        # Transferência Aprovada e sendo realizada
        ContaBancaria.contas[num_conta]['_saldo'] += valor_de_transferencia 
          
        taxa = round(valor_de_transferencia * ContaBancaria.taxa_juros, 2) # Arredondamento a taxa
    
        if pix:
            self._saldo -= valor_de_transferencia # Via pix, é sem taxa.
            pix = "via PIX"
        else:
            self._saldo -= ContaBancaria._formatar_numeros(taxa)
            pix = ""
        
        data, mes, ano, horario = ContaBancaria._obter_data_atual()
        
        # processo de verificar se o user já realizou alguma transferência para esse destinatário;
        contagem_enviado = 1
        contagem_recebido = 1
        for item in list(self._registro[2].keys()):
            if "ºN" in item and f"{conta_destino}" in item:
                contagem_enviado = _num_trans(item) + 1

        for item in list(ContaBancaria.contas[num_conta]["_registro"][2].keys()):
            if "ºN" in item and f"{self._numero_conta}" in item:
                contagem_recebido = _num_trans(item) + 1
                
        id_transicao = _gerar_id_transacao()
        # Registro de transferência no Remetente
        self._registro[2][f'{conta_destino}_{contagem_enviado}ºN'] = {
            "tipo": f"Transferência via PIX" if pix else "Transferência com Taxa",
            "destino": conta_destino,
            "data": f"{data} {mes} {ano} - {horario}",
            "valor": valor_de_transferencia if pix else taxa,
            "ID": id_transicao
        }

        # Registro de Transferência no Destinatário.
        ContaBancaria.contas[num_conta]["_registro"][2][f"{self._numero_conta}_{contagem_recebido}ºN"] = {
            "tipo": 'PIX Recebido' if pix else "Transferência Recebida",
            "Remetente": f"{self._numero_conta} - {self._nome}" ,
            "data": f"{data} {mes} {ano} - {horario}",
            "valor": valor_de_transferencia,
            "ID": id_transicao
        }    
        
        # Atualizando o contas! de acordo com o self
        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        
        
        # Duas mensagem diferente, a primeira sendo transferência padrão com taxa e a segunda e ultima com transferência
        # via pix
        return f'\033[1;33mTransferência Concluída\033[m com taxa\n'\
            f"Destinatário: {ContaBancaria.contas[num_conta]["_nome"]}\n"\
            f'Valor da Transferência: {valor_de_transferencia}\n'\
            f"\033[4;31mValor Extraído: {taxa}\033[m\n"\
            f'Seu Saldo Atual: {self._saldo}\n' \
            if not pix else \
            '\033[1;33mTransferência Concluída\033[m via Pix\n'\
            f"Destinatário: {ContaBancaria.contas[num_conta]["_nome"]}\n"\
            f'Valor da Transferência: {valor_de_transferencia}\n'\
            f'Valor Extraído: {valor_de_transferencia}\n'\
            f'Seu Saldo Atual: {self._saldo}\n'

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
        if not self._saldo >= valor_sacado:
            return f'\033[1;31mSaldo Insuficiente\033[m'
        
        self._saldo -= valor_sacado

        return f'\033[1;33mSaque Concluído\033[m\n'\
            f'Valor Sacado: {valor_sacado}\n'\
            f'Saldo Atual: {self._saldo}'
