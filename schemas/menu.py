from pydantic import BaseModel
from typing import Optional, List
from model.menu import Menu

# from schemas import MenuSchema


class MenuSchema(BaseModel):
    """ Define como um novo menu a ser inserido deve ser representado
    """
    id: Optional[int] = 1
    nome_alimento: str = "Filé com Fritas"
    cat_alimento: str = "Prato principal"
    desc_alimento: str = "Filé Mingnon acompanhado de arroz, feijão e batatas fritas"
    preco: float = 34.80


class MenuBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do prato.
    """
    nome_alimento: str = "Filé com Fritas"


class ListagemMenuSchema(BaseModel):
    """ Define como uma listagem de menus será retornada.
    """
    menus:List[MenuSchema]


def apresenta_menus(menus: List[Menu]):
    """ Retorna uma representação do menu seguindo o schema definido em
        MenuViewSchema.
    """
    result = []
    for menu in menus:
        result.append({
            "id": menu.id,
            "nome_alimento": menu.nome_alimento,
            "cat_alimento": menu.cat_alimento,
            "desc_alimento": menu.desc_alimento,
            "preco": menu.preco,
        })

    return {"menus": result}


class MenuViewSchema(BaseModel):
    """ Define como um menu será retornado: menu + menu.
    """
    id: int = 1
    nome_alimento: str = "Filé com Fritas"
    cat_alimento: str = "Prato principal"
    desc_alimento: str = "Filé Mingnon acompanhado de arroz, feijão e batatas fritas"
    preco: float = 34.80


class MenuDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_alimento: str

def apresenta_menu(menu: Menu):
    """ Retorna uma representação do menu seguindo o schema definido em
        MenuViewSchema.
    """
    return {
        "id": menu.id,
        "nome_alimento": menu.nome_alimento,
        "cat_alimento": menu.cat_alimento,
        "desc_alimento": menu.desc_alimento,
        "preco": menu.preco,
    }