from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
# from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column("pk_pedido", Integer, primary_key=True)
    mesa = Column(Integer, unique=False)
    responsavel = Column(String(140), unique=False)
    pedido = Column(String(300), unique=False)
    obs = Column(String(300), unique=False)
    status = Column(String(20), unique=False)
    valor = Column(Float, unique=False)
    data_insercao = Column(DateTime, default=datetime.now(), unique=False)

    # Definição do relacionamento entre o menu e um pedido.
    # Aqui está sendo definido a coluna 'pedido' que vai guardar
    # a referencia ao pedido, a chave estrangeira que relaciona
    # um pedido ao menu.
    # pedido = Column(Integer, ForeignKey("menu.pk_menu"), nullable=False)
    

    def __init__(self, mesa:int, responsavel:str, pedido:str, obs:str, status:str, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um pedido

        Arguments:
            mesa: numero da mesa
            responsavel: responsavel do pedido.
            status: status do pedido
            valor: valor do pedido
            data_insercao: data de quando o pedido foi inserido à base
        """
        self.mesa = mesa
        self.responsavel = responsavel
        self.pedido = pedido
        self.obs = obs
        self.status = status
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao is not None:
            try:
                self.data_insercao = datetime.strptime(data_insercao, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("data_insercao must be a string in the format 'YYYY-MM-DD HH:MM:SS'")

    # def adiciona_menu(self, menu:Menu):
    #     """ Adiciona um novo pedido ao menu
    #     """
    #     self.menus.append(menu)

