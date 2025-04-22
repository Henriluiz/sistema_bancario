from modules.models import ContaBancaria, Autenticator
import json
class DataStorage(ContaBancaria):    
    @staticmethod
    def carregar():
        # ContaBancaria.loading_animation("Carregando..")
        
        try:
            with open(ContaBancaria.FILE, 'r', encoding='utf-8') as file_:
                dados = json.load(file_, )
                print(f"1º {dados}")
            for item in dados:
                for itens in dados[item]:
                    if itens == "_senha":
                        dados[item]["_senha"] = Autenticator.descriptografar(dados[item]["_senha"])
                    if itens == "_pix":
                        pix_info = dados[item]["_pix"]
                        tipos_pix = ["pix_cpf", "pix_fone", "pix_email","pix_aleatoria"]
                        for tipo in tipos_pix:
                            if tipo in pix_info:
                                dados[item]["_pix"][tipo] = Autenticator.descriptografar(dados[item]["_pix"][tipo])
            
            ContaBancaria.contas = dados  # Substitui a lista de contas
            print(f"2º{dados}")
            return "\033[1;32mDados carregados com sucesso!\033[m"
        except FileNotFoundError:
            return "\033[1;31mArquivo não encontrado.\033[m"
        except Exception as e:
            return f"\033[1;31mErro ao carregar dados: {e}\033[m"

    @classmethod
    def salvar(cls):
        # ContaBancaria.loading_animation("Salvando")
        """
        Adiciona um novo dicionário a um arquivo JSON existente.

        Args:
            arquivo (str): Nome do arquivo JSON.
            novo valor (dict): Dicionário a ser adicionado.
        """
        # Criptografando dados sigilosos 
        for item in cls.contas:
            for itens in cls.contas[item]:
                if itens == "_senha":
                    cls.contas[item]["_senha"] = cls.criptografar(cls.contas[item]["_senha"])
                if itens == "_pix":
                    pix_info = cls.contas[item]["_pix"]
                    tipos_pix = ["pix_cpf", "pix_fone", "pix_email","pix_aleatoria"]
                    for tipo in tipos_pix:
                        if tipo in pix_info:
                            cls.contas[item]["_pix"][tipo] = cls.criptografar(cls.contas[item]["_pix"][tipo])
        
        with open(cls.FILE, 'w', encoding='utf-8') as arquivo:
            json.dump(cls.contas, arquivo, indent=4, ensure_ascii=False)
        ContaBancaria.limpar_terminal(True)
