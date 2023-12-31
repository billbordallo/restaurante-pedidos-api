from sqlalchemy import Column, String, Integer, Float
from model import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column("pk_menu", Integer, primary_key=True)
    nome_alimento = Column(String(140), unique=True)
    cat_alimento = Column(String(140))
    desc_alimento = Column(String(500))
    preco = Column(Float)


    def __init__(self, nome_alimento:str, cat_alimento:str, desc_alimento:str, preco:float):
        """
        Cria um Menu

        Arguments:
            nome_alimento: o nome do prato/alimento (ex.: "Filé com Fritas").
            cat_alimento: categoria do alimento (ex.: "Pratos principais").
            des_alimento: descrição do alimento (ex.: "Filé Mingnon acompanhado de arroz, feijão e batatas fritas").
            preco: preço do item (ex.: "34.80").
        """
        self.nome_alimento = nome_alimento
        self.cat_alimento = cat_alimento
        self.desc_alimento = desc_alimento
        self.preco = preco
