# app.py
from modules.transacao import Transacao
from modules.data_storage import DataStorage
from pprint import pprint

DataStorage.carregar()
a = Transacao()
# print(a.depositar(1000000))
print(a.desbloquear_conta("A12345@!"))
# ! E pensa em uma forma de ao imprimir a fatura, não apareça os 
# ! itens já pagos!
# print(a.parcela_divida(1050))
# print(a.quitar_divida()) 
# a.pix = "luizao@gmail.com"
# print(a._pix)
# print(a.abrir_chave_pix(1, "53421414866"))
# print(a.abrir_chave_pix())
# print(a.solicitar_cartao_credito())
# print(a.compra_com_debito("Chuteira", 530())
# print(a.compra_com_deb))
# print(a.compra_com_debito("Meião", 50))
# print(a.transferir("5db2b93c-49a8-4271-a222-b00ef36d204c", 50))
# print(a.consultar_extrato())
# print(a.solicitar_cartao_credito())
# print(a.compra_com_credito("Moto quebrada", 1203))
# print(a.compra_com_credito("Lampada moto", 203))
print(a.compra_com_credito("MOTO ELÉTRICA", 4100))
# print(a.compra_com_credito("Cadeira", 4903))
# print(a.compra_com_credito("Óculos", 3903))
# print(a.compra_com_debito("Mouse", 960))
# print(a.compra_com_debito("Luva", 140))
# print(a.compra_com_debito("Cinema", 102090))
# print(a.gerar_pdf())
d = input("Sair: ")
DataStorage.salvar()