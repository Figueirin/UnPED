class Produto:
    """
    Representa um item do cardápio (Café, Pão de Queijo, etc.).
    Guarda as informações gerais do produto (nome e preço de venda).

    28/05 - Adicionada numero indetificador do produto e categoria.
    """
    def __init__(self, id_produto, nome_produto, preco, categoria):
        self.nome = nome_produto
        self.preco = preco
        self.id = id_produto
        self.categoria = categoria

    def to_dict(self):
        # Converte o objeto para um dicionário simples (usado para salvar em JSON mais tarde)
        return {
            "nome": self.nome,
            "preco": self.preco,
            "id": self.id,
            "categoria": self.categoria

        }
    
    def __str__(self):
        # Mostra o produto formatado com duas casas decimais no preço (ex: Café R$4.50)
        return f"[{self.id}] |{self.nome} | R${self.preco:.2f}"

    