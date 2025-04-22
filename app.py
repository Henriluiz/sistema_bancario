# app.py
from modules.transacao import Transacao
from modules.data_storage import DataStorage
from pprint import pprint

print(DataStorage.carregar())
a = Transacao()
# print(a.depositar(100))
print(a.desbloquear_conta("A12345@!"))
# print(a.parcela_divida())
# print(a.quitar_divida())
# a.pix = "luizao@gmail.com"
# print(a._pix)
# print(a.abrir_chave_pix(1, "53421414866"))
print(a.abrir_chave_pix())
# print(a.so¹licita¹r_cartao_crediito("Luva", 250.2))
# print(a.compra_com_debito("Chuteira", 530to())
# print(a.compra_com_deb))
# print(a.compra_com_debito("Meião", 50))
# print(a.transferir("2", 50)) #! No momento atuando nesse!
# print(a.consultar_extrato()) 
# print(a.solicitar_cartao_credito())
# print(a.compra_com_credito("Avião", 10090))
# print(a.compra_com_credito("PC gamer", 13490))
# print(a.compra_com_credito("Cinema", 90))
# print(a.gerar_pdf())
d = input("Sair: ")
DataStorage.salvar()