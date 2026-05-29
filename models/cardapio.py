from models.produto import Produto

class Cardapio:
    """
    Gerencia a coleção de produtos disponíveis para venda no bar/restaurante.
    Esta classe é responsável por cadastrar, listar de forma categorizada e buscar produtos.
    """
    def __init__(self):
        """
        Construtor da classe Cardapio.
        Inicializa uma lista vazia para armazenar os objetos de Produto.
        """
        self.produtos = []

    def add_produto(self, produto):
        """
        Cadastra um novo objeto Produto no catálogo do cardápio.
        Retorna True se cadastrado com sucesso, False se for duplicado (ID ou Nome).
        """
        for p in self.produtos:
            if str(p.id) == str(produto.id) or p.nome.lower() == produto.nome.lower():
                return False
        self.produtos.append(produto)
        return True
    
    def listar_produtos(self):
        """
        Exibe todos os produtos cadastrados no cardápio organizados e agrupados por categorias.
        Se o cardápio estiver vazio, não imprime nada ou passa direto.
        """
        # Dicionário temporário para mapear { nome_categoria: [lista_de_produtos] }
        categorias = {}
        for produto in self.produtos:
            cat = produto.categoria
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(produto)

        # Exibe os produtos de forma estruturada e elegante no console
        for categoria, itens in categorias.items():
            print(f"\n === {categoria.upper()} ===")
            for produto in itens:
                print(f"{produto}")

    def buscar_produto(self, termo):
        """
        Busca um produto cadastrado no cardápio.
        A busca aceita tanto o ID numérico (como string ou int) quanto o nome exato (case-insensitive).
        
        Parâmetros:
        - termo (str/int): O termo de busca (ID ou Nome do produto).
        
        Retorna:
        - Produto: O objeto Produto se for encontrado, ou None caso contrário.
        """
        termo_str = str(termo).strip().lower()
        for produto in self.produtos:
            # Compara tanto com o ID quanto com o nome convertido em minúsculas
            if str(produto.id) == termo_str or produto.nome.lower() == termo_str:
                return produto

        # Caso o loop termine sem achar nenhum correspondente
        return None
