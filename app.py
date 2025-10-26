# app.py

# Importações centralizadas para inicialização do projeto

from modules.models import ContaBancaria, Autenticator
from modules.transacao import Transacao
from modules.interface import App
from modules.data_storage import DataStorage
from modules.pdf_gen import PDF

# Inicialização do projeto (exemplo)
if __name__ == "__main__":
    # Aqui você pode iniciar a interface, criar contas, etc.
    # Exemplo:
    interface = App()
    interface.mainloop()
    pass

DataStorage.carregar()
# a = Transacao()
# # print(a.depositar(1000000))
# print(a.desbloquear_conta("A12345@!"))

# ! E pensa em uma forma de ao imprimir a fatura, não apareça os 
# ! itens já pagos!
# print(a._consultar_total_fatura())
# print(a.pagar_fatura())
# print(a._consultar_fatura_nao_paga(15, 10))
# print(a.quitar_divida()) 
# a.pix = "luizao@gmail.com"
# print(a._pix)
# print(a.abrir_chave_pix(1, "53421414866"))
# print(a.abrir_chave_pix())
# print(a.depositar(1500))
# print(a.solicitar_cartao_credito())
# print(a.compra_com_debito("Chuteira", 5100))
# print(a.compra_com_deb))
# print(a.compra_com_debito("Meião", 50))
# print(a.transferir("5db2b93c-49a8-4271-a222-b00ef36d204c", 50))
# print(a.consultar_extrato())
# print(a.solicitar_cartao_credito())
# print(a.compra_com_credito("Chuteira", 4203))
# print(a.compra_com_credito("Lampada moto", 203))
# print(a.compra_com_credito("ROUPA NOVAS", 200))
# print(a.compra_com_credito("Cadeira", 4903))
# print(a.compra_com_credito("Óculos", 3903))
# print(a.compra_com_debito("Mouse", 960))
# print(a.compra_com_debito("Luva", 140))
# print(a.compra_com_debito("Cinema", 102090))
# print(a.gerar_pdf())
d = input("Sair: ")
DataStorage.salvar()