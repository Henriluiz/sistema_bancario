import customtkinter as ctk
from .transacao import Transacao


class App(ctk.CTk):
    app = ctk.CTk
    def __init__(self):
        super().__init__()
        self.title("Banco em Python")
        self.geometry("500x500")

        # Criando conta e transação
        self.transacao = Transacao.__new__(Transacao)
        
        print(self.transacao.contas)
        
        label_usuario = ctk.CTkLabel(self, text="Digite o Nº da conta: ").pack(pady=10)
        entrada_conta = ctk.CTkEntry(self, placeholder_text="Digite o número: ")
        entrada_conta.pack(pady=0)
        
        label_senha = ctk.CTkLabel(self, text="Digite a sua senha: ").pack(pady=10)
        entrada_senha = ctk.CTkEntry(self, placeholder_text="Senha: ")
        entrada_senha.pack(pady=0)
        
        ctk.CTkButton(self, text="Login", command=lambda: self.transacao.login(entrada_conta.get(), entrada_senha.get())).pack(pady=10)
        
    def tela_principal(self):
        # Tela principal
        self.lbl_saldo = ctk.CTkLabel(self, text=f"Saldo: {self.transacao._saldo}")
        self.lbl_saldo.pack(pady=10)

        ctk.CTkButton(self, text="Depositar", command=self.janela_deposito).pack(pady=5)
        ctk.CTkButton(self, text="Sacar", command=self.janela_saque).pack(pady=5)
        ctk.CTkButton(self, text="Transferir", command=self.janela_transferencia).pack(pady=5)
        ctk.CTkButton(self, text="Extrato", command=self.mostrar_extrato).pack(pady=5)

        self.lbl_msg = ctk.CTkLabel(self, text="", text_color="green")
        self.lbl_msg.pack(pady=20)
        
    def atualizar_saldo(self):
        self.lbl_saldo.configure(text=f"Saldo: {self.transacao._saldo}")

    
    def janela_deposito(self):
        janela = ctk.CTkInputDialog(text="Digite valor do depósito:", title="Depositar")
        valor = janela.get_input()
        if valor:
            msg = self.transacao.depositar(float(valor))
            self.lbl_msg.configure(text=msg)
            self.atualizar_saldo()

    def janela_saque(self):
        janela = ctk.CTkInputDialog(text="Digite valor do saque:", title="Sacar")
        valor = janela.get_input()
        if valor:
            msg = self.transacao.sacar(float(valor))
            self.lbl_msg.configure(text=msg)
            self.atualizar_saldo()

    def janela_transferencia(self):
        janela_conta = ctk.CTkInputDialog(text="Conta destino:", title="Transferência")
        conta_destino = janela_conta.get_input()
        janela_valor = ctk.CTkInputDialog(text="Valor da transferência:", title="Transferência")
        valor = janela_valor.get_input()
        if conta_destino and valor:
            msg = self.transacao.transferir(conta_destino, float(valor))
            self.lbl_msg.configure(text=msg)
            self.atualizar_saldo()

    def mostrar_extrato(self):
        self.transacao.consultar_extrato()
        self.lbl_msg.configure(text="Extrato mostrado no console")

if __name__ == "__main__":
    app = App()
    app.mainloop()
