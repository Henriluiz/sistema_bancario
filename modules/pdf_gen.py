from fpdf import FPDF
from locale import setlocale, currency, LC_ALL


def formatar_numero(numero):
    # Configura a localização para o Brasil
    setlocale(LC_ALL, 'pt_BR.UTF-8')
    # Formata como moeda (R$ 300.230,00)
    return currency(numero, symbol=True, grouping=True)

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
            self.cell(largura_valor, 10, f"{formatar_numero(valor)}", border=1, align='R', fill=fill)
            self.ln()
            fill = not fill  # Inverte o preenchimento para a próxima linha

        self.ln(5)

        # Linha de total destacada (também centralizada)
        total = sum(registro.values())
        self.set_x(start_x)
        self.set_font("Arial", 'B', 12)
        self.cell(largura_item, 10, 'Total', border=1)
        self.cell(largura_valor, 10, f"{formatar_numero(total)}", border=1, align='R')
