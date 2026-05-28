from models.produto import Produto

class Cardapio:
    """
    Gerencia a coleção de produtos à venda no bar/restaurante.
    """
    def __init__(self):
        # Inicializa a lista vazia de produtos cadastrados no sistema
        self.produtos = []

    def add_produto(self, produto):
        # Cadastra um novo produto no cardápio
        self.produtos.append(produto)
    
    def listar_produtos(self):
        # Exibe todos os produtos do cardápio um a um
        categorias = {}
        for produto in self.produtos:
            cat = produto.categoria
            
            if cat not in categorias:
                categorias[cat] = []
            
            categorias[cat].append(produto)

        for categoria, itens in categorias.items():
            print(f"\n === {categoria.upper()} ===")

            for produto in itens:
                print(f"{produto}")

    def buscar_produto(self, termo):
        termo_str = str(termo).strip().lower()
        for produto in self.produtos:
            if str(produto.id) == termo_str or produto.nome.lower() == termo_str:
                return produto

        return None

