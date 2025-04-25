# Sistema Bancário em Terminal (Python)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![CLI](https://img.shields.io/badge/Interface-Command%20Line-brightgreen)

Um sistema bancário completo com operações CRUD, autenticação segura e persistência de dados, totalmente operacional no terminal.

## 🚀 Funcionalidades Principais

- **Autenticação Segura**
  - Criptografia/Descriptografia de senhas
  - Validação de força de senhas
  - Limite de tentativas

- **Operações Bancárias**
  - Depósitos, saques e transferências (PIX/TED)
  - Cartão de crédito com limite calculado
  - Controle de dívidas e parcelamento
  - Extrato detalhado com histórico

- **Gerenciamento de Conta**
  - Bloqueio/desbloqueio de conta
  - Cadastro de chaves PIX (CPF/Email/Telefone)
  - Cálculo de juros
  - Persistência em JSON

## ⚙️ Tecnologias

- Python 3.x
- Módulos padrão:
  - `json` para armazenamento
  - `re` para validação de padrões
  - `datetime` para registros temporais
- Criptografia customizada com substituição de caracteres

## 📋 Estrutura de Classes

# Estrutura do Sistema Bancário

Este projeto consiste em um sistema bancário modularizado com as seguintes classes principais:

## Diagrama de Classes Simplificado
```
Autenticator  
├─ ContaBancaria  
   ├─ DataStorage  
   ├─ Transacao  
   └─ PDF (classe auxiliar)  
```

---

## 1. Autenticator (Módulo de Segurança)

**Responsabilidade**: Criptografia de senhas e validação de segurança

```python
class Autenticator:
    # Dicionários para substituição de caracteres
    chaves_especiais = {...}
    chave_alf_car = {...}

    @classmethod
    def criptografar(cls, senha)
    @classmethod
    def descriptografar(cls, senha_criptografada)
    @staticmethod
    def validar_senha(senha)
    def auth_senha(self, senha="", conta=False)
```

---

## 2. ContaBancaria (Classe Principal)

**Responsabilidade**: Gerenciamento central de contas bancárias

```python
class ContaBancaria(Autenticator):
    # Principais atributos:
    - contas (class attribute): Dicionário de todas as contas
    - _numero_conta, _saldo, _pix, _registro, etc.

    # Principais métodos:
    def __init__(self, num_conta="")
    def bloquear_conta(self)
    def desbloquear_conta(self, senha="")
    def compra_com_credito(self, item="", valor_compra=0.0)
    def compra_com_debito(self, item="", valor_compra=0.0)
    def solicitar_cartao_credito(self)
    def abrir_chave_pix(self, metodo=1, nova_chave="")
    @classmethod
    def buscar_por_numero(cls, numero_conta)
```

---

## 3. DataStorage (Persistência de Dados)

**Responsabilidade**: Carregar/Salvar dados em JSON com criptografia

```python
class DataStorage(ContaBancaria):
    @staticmethod
    def carregar()
    @classmethod
    def salvar(cls)
```

---

## 4. Transacao (Operações Financeiras)

**Responsabilidade**: Gerenciar transações bancárias

```python
class Transacao(ContaBancaria):
    def depositar(self, valor_depositar=0.0)
    def transferir(self, conta_destino="", valor_de_transferencia=0.0)
    def sacar(self, valor_sacado=0.0)
```

---

## 5. PDF (Relatórios)

**Responsabilidade**: Geração de documentos financeiros

```python
class PDF(FPDF):
    def header(self)
    def footer(self)
    def fatura(self, numero_conta, registro)
```

---

## Fluxo Principal

1. **Inicialização**:
   - Carrega dados existentes (`DataStorage.carregar()`)
   - Cria nova conta (`ContaBancaria()`)

2. **Operações**:
   - Transações (`Transacao.transferir()`, `.depositar()`, `.sacar()`)
   - Compras (crédito/débito)
   - Gerenciamento de conta (bloqueio/PIX/cartão)

3. **Persistência**:
   - Salva alterações (`DataStorage.salvar()`)
   - Gera PDFs (`PDF.fatura()`)

---

## Dependências Principais

- `fpdf`: Geração de PDFs  
- `keyboard`: Controle de teclado (limpeza de terminal)  
- `pprint`: Formatação de saída  
- `locale`: Formatação monetária

---

## Exemplo de Uso

```python
# app.py
from modules.transacao import Transacao
from modules.data_storage import DataStorage

# Carrega dados
print(DataStorage.carregar())

# Cria conta e realiza operações
conta = Transacao()
conta.desbloquear_conta("SenhaSegura123!")
conta.depositar(1500.00)
conta.transferir("123456", 300.00)

# Salva alterações
DataStorage.salvar()
```

---

Esta estrutura permite uma clara separação de responsabilidades e facilita a manutenção e expansão do sistema.


## 🔒 Segurança
- Todas as senhas são criptografadas antes do armazenamento
- Validação rigorosa de:
  - Formato de chaves PIX
  - Força de senhas (requer 2+ caracteres especiais e números)
  - Bloqueio após 3 tentativas falhas

# 📌 Melhorias Futuras
- Adicionar interface web com Flask/Django
- Implementar banco de dados SQL
- Adicionar sistema de investimentos
- Criar relatórios PDF

#### Note: Projeto desenvolvido para fins educacionais, demonstrando conceitos avançados de POO em Python.
