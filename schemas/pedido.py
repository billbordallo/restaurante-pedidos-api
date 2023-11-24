from pydantic import BaseModel
from typing import Optional, List
from model.pedido import Pedido

# from schemas import PedidoSchema


class PedidoSchema(BaseModel):
    """ Define como um novo pedido a ser inserido deve ser representado
    """
    id: Optional[int] = 1
    mesa: int = 35
    responsavel: str = "João"
    pedido: str = "Filé com Fritas"
    obs: str = "Ao ponto"
    status: str = "Aguardando"
    valor: float = 35.90
    data_insercao: Optional[str] = "2023-11-01 12:00:00"


class PedidoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do pedido.
    """
    id: int = 5

class PedidoNomeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do pedido.
    """
    pedido: str = "Filé com Fritas"    

class PedidoAtualizaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca e a atualização do status.
      Que será feita apenas com base no id do pedido.
    """
    id: int = 5
    status: str = "Aguardando"

class ListagemPedidoSchema(BaseModel):
    """ Define como uma listagem de pedidos será retornada.
    """
    pedidos:List[PedidoSchema]


def apresenta_pedidos(pedidos: List[Pedido]):
    """ Retorna uma representação do pedido seguindo o schema definido em
        PedidoViewSchema.
    """
    result = []
    for pedido in pedidos:
        result.append({
            "id": pedido.id,
            "mesa": pedido.mesa,
            "responsavel": pedido.responsavel,
            "pedido": pedido.pedido,
            "obs": pedido.obs,
            "status": pedido.status,
            "valor": pedido.valor,
            "data_insercao": pedido.data_insercao,
        })

    return {"pedidos": result}


class PedidoViewSchema(BaseModel):
    """ Define como um pedido será retornado.
    """
    id: int = 1
    mesa: int = 35
    responsavel: str = "João"
    pedido: str = "Filé com Fritas"
    obs: str = "Ao ponto"
    status: str = "Em preparo"
    valor: float = 35.90
    data_insercao: Optional[str] = "2023-11-01 12:00:00"
    # menu:List[PedidoSchema]


class PedidoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    pedido: str
    mesa: int
    responsavel: str

def apresenta_pedido(pedido: Pedido):
    """ Retorna uma representação do pedido seguindo o schema definido em
        PedidoViewSchema.
    """
    return {
        "id": pedido.id,
        "mesa": pedido.mesa,
        "responsavel": pedido.responsavel,
        "pedido": pedido.pedido,
        "obs": pedido.obs,
        "status": pedido.status,
        "valor": pedido.valor,
        "data_insercao": pedido.data_insercao
        }
