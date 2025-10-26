from .models import ContaBancaria
from .models import DataStorage, linha, abreviar_mes, numero_do_mes, Decimal


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
        
        # Processo de verificar se o user já realizou alguma transferência para esse destinatário;
        contagem_enviado = 1
        contagem_recebido = 1
        for item in list(self._registro[2].keys()):
            if "ºN" in item and f"{num_conta}" in item:
                contagem_enviado = ContaBancaria._num_trans(item) + 1

        for item in list(ContaBancaria.contas[num_conta]["_registro"][2].keys()):
            if "ºN" in item and f"{self._numero_conta}" in item:
                contagem_recebido = ContaBancaria._num_trans(item) + 1
                
        id_transicao = ContaBancaria._gerar_id()
        # Registro de transferência no Remetente
        self._registro[2][f'{num_conta}_{contagem_enviado}ºN'] = {
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
    
    def compra_com_credito(self, item, valor_compra): # > Testado!
        """ Uso do cartão de crédito

        Args:
            item (str): Nome do Produto ou Serviço
            valor_compra (int): valor total do item

        Returns:
            _type_: _description_
        """
        linha("Pagamento com Crédito!")
        try:
            saldo = self._saldo
        except AttributeError:
            return '\033[1;31mSua Instância não tem os dados necessário. Use ContaBancaria primeiro e cadastre todas as informações necessária lá!\033[m'
        
        if not self._credito:
            return f"\033[1;31mVocê não tem o cartão de crédito, tente usa o solicitar_cartao_credito\033[m"

        # Controle de Entradas
        if not item or not valor_compra:
            while True:
                try:
                    item = str(input("Digite o nome do item da compra: "))
                    valor_compra = int(input(f'Digite o valor de {item}: R$'))
                except Exception:
                    print('\033[1;31mDigite apenas texto na primeira entrada e float na segunda!\033[m')
                else:
                    break
        else:
            try:
                valor_compra = int(valor_compra)
                if not isinstance(item, str) and isinstance(valor_compra, int):
                    return "\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m"
            except Exception:
                print('\033[1;31mDigite apenas texto no primeiro argumento e float no segundo argumento\033[m')

        # Verificação de limite, se o valor da compra for maior que o limite, a compra será bloqueada!
        if valor_compra > ContaBancaria.contas[self._numero_conta]["_limite_atual"] or valor_compra > self._limite_atual:
            return f"\033[1;31mO limite foi excedido!\033[m"
        
        valor_parcela, vezes_max = Transacao._divisao_parcelas(valor_compra)
        
        data, mes, ano, horario = ContaBancaria._obter_data_atual()
        
        id = ContaBancaria._gerar_id()
        
        self._registro[0][f'{item}_{id.split("-")[1]}'] = {
            "Tipo": f"Compra no Crédito",
            "Produto": item,
            "Data": f"{data} {mes} {ano} - {horario}",
            "Valor": f"{ContaBancaria._numero_em_reais(valor_compra)}",
            "Parcelas": f"{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}",
            "ID": id
        }
        
        ano = int(str(ano)[2:4])
        if data > 7:
            mes += 1 # Condição trata do próximo mês
            while True:
                try:
                    if vezes_max == 0:
                        print("SAI 2")
                        break
                    self._registro[3][f'PRÓXIMO {abreviar_mes(mes)}/{ano}'][f"{item}x{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}x{id}"] = {
                        "Tipo": f"Compra no Crédito",
                        "Produto": item,
                        "Data": f"{data} {mes} {ano} - {horario}",
                        "Parcelas": f"{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}",
                        "ID": id
                    }
                    mes += 1
                    vezes_max -= 1
                    if mes == 13:
                        mes = 1
                        ano += 1

                except KeyError:
                    self._registro[3][f'PRÓXIMO {abreviar_mes(mes)}/{ano}'] = {}
        
        else:
            while True:
                try:
                    self._registro[3][f'ATUAL {abreviar_mes(mes)}/{ano}'][f"{item}x{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}x{id}"] = {
                        "Tipo": f"Compra no Crédito",
                        "Produto": item,
                        "Data": f"{data} {mes} {ano} - {horario}",
                        "Parcelas": f"{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}",
                        "ID": id
                    }
                    mes += 1
                    vezes_max -= 1
                    break
                except KeyError:
                    self._registro[3][f'ATUAL {abreviar_mes(mes)}/{ano}'] = {}
                    
            if vezes_max > 1:
                if mes == 13:
                    mes = 1
                    ano += 1
                while True:
                    try:
                        if vezes_max == 0:
                            break
                        self._registro[3][f'PRÓXIMO {abreviar_mes(mes)}/{ano}'][f"{item}x{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}x{id}"] = {
                            "Tipo": f"Compra no Crédito",
                            "Produto": item,
                            "Data": f"{data} {mes} {ano} - {horario}",
                            "Parcelas": f"{ContaBancaria._numero_em_reais(valor_parcela)}x{vezes_max}",
                            "ID": id
                        }
                        mes += 1
                        vezes_max -= 1
                        if mes == 13:
                            mes = 1
                            ano += 1
                    except KeyError:
                        self._registro[3][f"PRÓXIMO {abreviar_mes(mes)}/{ano}"] = {}
                        
        self._divida_ativa += Decimal(valor_compra)
        
        self._limite_atual -= Decimal(valor_compra)
        
        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        
        return f'\033[1;33mCOMPRA EFETUADA COM SUCESSO\033[m\nItem: {item}\nValor: {valor_compra}\n'

    def compra_com_debito(self, item="", valor_compra=0.0): # > Testado!
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
        
        if self._saldo < valor_compra:
            return "\033[1;31mSaldo Insuficiente!\033[m"
        
        data, mes, ano, horario = ContaBancaria._obter_data_atual()
        
        contagem_enviado = 1
        for item_ in list(self._registro[1].keys()):
            if "ºN" in item_ and f"{item}" in item_:
                contagem_enviado = ContaBancaria._num_trans(item_) + 1
        
        id = ContaBancaria._gerar_id()
        
        self._registro[1][f'{item}_{contagem_enviado}ºN'] = {
            "Tipo": f"Compra no Débito",
            "Produto": item,
            "Data": f"{data} {mes} {ano} - {horario}",
            "Valor": f"{ContaBancaria._numero_em_reais(valor_compra)}",
            "ID": id
        }
        self._saldo -= valor_compra
        
        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        
        return f'\033[1;33mCOMPRA EFETUADA COM SUCESSO\033[m\nItem: {item}\nValor: {valor_compra}\nSaldo Atual: {ContaBancaria.contas[self.numero_conta]["_saldo"]}'
    
    def quitar_divida(self):
        linha("Quitar Dívida!")
        
        if self._divida_ativa == 0.0:
            return f'\033[1;32mNão se preocupe, você não tem nenhuma dívida.\033[m\nDívida: {self._divida_ativa}\n'
        elif self._divida_ativa > self._saldo:
            return '\033[1;31mSALDO INSUFICIENTE, tente usa o parcela divida.\033[m'
        
        print(f"Sua dívida: {self._divida_ativa}")
        
        data, mes, ano, horario = ContaBancaria._obter_data_atual()
        
        contagem_enviado = 1
        for item_ in list(self._registro[2].keys()):
            if "PAG" in item_ and "ºN" in item_ and f"{data} {mes} {ano}" in item_:
                contagem_enviado = ContaBancaria._num_trans(item_) + 1
        
        id = ContaBancaria._gerar_id()
        
        self._registro[2][f'PAG {data} {mes} {ano}_{contagem_enviado}ºN'] = {
            "Tipo": f"Pagamento dívida",
            "Porcentagem": "100%",
            "Valor": f"{ContaBancaria._numero_em_reais(self._divida_ativa)}",
            "Data": f"{data} {mes} {ano} - {horario}",
            "ID": id,
        }
        
        # Pagando todas as faturas pendentes/próximas e atual.
        for item in self._registro[3]:
            titulo = str(item).split(" ")[0]
            mes, ano = str(item).split(" ")[1].split("/")
            if titulo == "PENDENTE" or titulo == "PRÓXIMO":
                self._registro[3][f"PAGA {abreviar_mes(mes)}/{ano}"] = self._registro[3].pop(f"{titulo} {abreviar_mes(mes)}/{ano}")

        
        self._saldo -= Decimal(self._divida_ativa)
        self._saldo = Decimal(ContaBancaria._formatar_numeros(self._saldo))
        self._divida_ativa = Decimal(0)
    
        self._limite_atual = self._limite

        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        return f'Sua dívida foi quitada, seu saldo ficou: {self._saldo}'
    
    def _divisao_parcelas(valor, max_par):
        """ Essa função controlará a divisão das parcelas, como valor e quantidade máxima de parcelas que será permitida por compra dependedo do valor.

        Args:
            valor (int): valor da compra.
            max_vez (int, optional): máximo de parcelas.
        Returns:
            tuple: Valor da Parcela, quantidade de vezes parceladas.
        """
        # * Garantindo que o "valor" seja inteiro
        try:
            valor = int(valor)
        except Exception:
            return False
        
        if max_par:
            # * Controle de quantidade máxima de vezes
            if valor <= 100:
                max_par = 1
            elif valor >= 100 and valor <= 199:
                max_par = 2
            elif valor >= 200 and valor <= 499:
                max_par = 3
            elif valor >= 500 and valor <= 999:
                max_par = 5
            elif valor >= 1000 and valor <= 1999:
                max_par = 6
            elif valor >= 2000 and valor <= 3499:
                max_par = 8
            elif valor > 3500 and valor <= 4999:
                max_par = 10
            elif valor >= 5000 and valor <= 7500:
                max_par = 12
            else:
                while True: # Permite que apenas o número máximo de parcela seja com parcelas de 400
                    est_valor_parcela = int(valor / max_par)
                    if max_par == 24: # O máximo será de 24 parcelas, em crédito puro!
                        break
                    if est_valor_parcela > 400:
                        max_par += 1
                    else:
                        print(f"Preço: {est_valor_parcela}x{max_par}")
                        break
        else:
            # * A escolha do usuário sobre a quantidade de parcelas
            while True:
                try:
                    num_parcelas = int(input(f"Digite quantas parcelas deseja [Máximo de {max_par} parcelas]: "))
                except KeyboardInterrupt:
                    return False
                except Exception:
                    print("\033[1;31mDigite apenas números inteiros!\033[m")
                else:
                    if num_parcelas > 0 and num_parcelas <= max_par:
                        valor_parcela = round(valor / num_parcelas, 2) 
                        print(f"\033[1;33mValor de cada parcela [{num_parcelas}x]: {ContaBancaria._numero_em_reais(valor_parcela)}\033[m")
                        confirmar = str(input("Aperte enter ou [N - para Cancelar]: "))
                        if len(confirmar) == 0:
                            break
                    else:
                        if num_parcelas > max_par:
                            print(f"\033[1;31mO número máximo de parcelas({max_par}x) foi ultrapassado!\033[m")
                        else:
                            print("\033[1;31mNão é permitido usa número negativo!\033[m")
        return valor_parcela, num_parcelas
    
    def pagar_fatura(self, mes: int=0, ano: int=0):
        """Pagar dívida
        
        Args:
            mes (int, optional): MM - Mês da fatura que será paga.
            ano (int, optional): AAAA - Ano da fatura que será paga.

        Returns:
            str: confirmação escrita
        """
        linha("Parcelar dívida!")
        if self._divida_ativa == 0.0:
            return f'\033[1;32mNão se preocupe, você não tem nenhuma dívida.\033[m\nDívida: {self._divida_ativa}\n'
        
        if not mes:
            print("Digite abaixo os dados necessário para pagar a fatura desejada.")
            while True:
                mes = int(input("MÊS [MM]: "))
                ano = int(input("ANO [AAAA]: "))
                if mes > 12 or mes < 0:
                    print("\033[1;31mTente novamente. Número do mês entre 1-12\033[m")
                elif ano < 2020:
                    print("\033[1;31mTente novamente. Com ano acima de 2020.\033[m")
                else:
                    break
        
        # Requerimentos necessários
        valor = ContaBancaria._consultar_total_fatura(mes, ano)
        if not valor:
            print("Digite ")
            return False
        
        
        # Se o valor for igual a divida, significa que o user usou o método incorreto para operação necessário, isso corrigir esse problema, para ter um registro certo no histórico dela
        data, mes_atual, ano_atual, horario = ContaBancaria._obter_data_atual()
        ano_atual = int(str(ano)[2:4])
        

        id = ContaBancaria._gerar_id()
        
        self._registro[2][f'PAR {data} {mes_atual} {ano_atual} {horario}'] = {
            "Tipo": f"Fatura de ",
            "Valor": f"{ContaBancaria._numero_em_reais(valor)} - {ContaBancaria._numero_em_reais(self._divida_ativa)}",
            "Data": f"{data} {mes} {ano} - {horario}",
            "ID": id,
        }
        
        self._divida_ativa -= Decimal(valor) # Pagar dívida
        self._saldo -= Decimal(valor) # Atualizar saldo
        
        # Aumentando o limite_atual sem ultrapassa o limite
        self._limite_atual = min(self._limite_atual + valor, self._limite)

        ContaBancaria.contas[self._numero_conta] = {chave: valor for chave, valor in self.__dict__.items() if chave != "_numero_conta"}
        return f"Saldo: \033[1;31m{self._saldo}\033[m\nDívida total: \033[1;31m{self._divida_ativa}\033[m"

# ContaBancaria._consultar_fatura_nao_paga()