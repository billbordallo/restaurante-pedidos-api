from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Menu, Pedido
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API de pedidos para restaurantes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pedido_tag = Tag(name="Pedido", description="Adição, visualização e remoção de pedidos à base")
menu_tag = Tag(name="Menu", description="Adição de um item aos alimentos cadastrados na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/pedido', tags=[pedido_tag],
          responses={"200": PedidoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pedido(form: PedidoSchema):
    """Adiciona um novo Pedido à base de dados

    Retorna uma representação do pedido.
    """
    
    pedido_feito = Pedido(
        mesa=form.mesa,
        responsavel=form.responsavel,
        pedido=form.pedido,
        obs=form.obs,
        status=form.status,
        valor=form.valor,
        data_insercao=form.data_insercao)
    logger.debug(f"Adicionando pedido de nome: '{pedido_feito.pedido}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pedido
        session.add(pedido_feito)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pedido de nome: '{pedido_feito.pedido}'")
        return apresenta_pedido(pedido_feito), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pedido de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pedido '{pedido_feito.pedido}', {error_msg}, {e}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pedido '{pedido_feito.pedido}', {error_msg}, {e}")
        return {"mesage": error_msg}, 400


@app.get('/pedidos', tags=[pedido_tag],
         responses={"200": ListagemPedidoSchema, "404": ErrorSchema})
def get_pedidos():
    """Faz a busca por todos os Pedidos cadastrados

    Retorna uma representação da listagem de pedidos.
    """
    logger.debug(f"Coletando pedidos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedidos = session.query(Pedido).all()

    if not pedidos:
        # se não há pedidos cadastrados
        return {"pedidos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(pedidos))
        # retorna a representação de pedido
        print(pedidos)
        return apresenta_pedidos(pedidos), 200


@app.get('/pedido', tags=[pedido_tag],
         responses={"200": PedidoViewSchema, "404": ErrorSchema})
def get_pedido(query: PedidoBuscaSchema):
    """Faz a busca por um Pedido a partir do id do pedido

    Retorna uma representação dos pedidos e comentários associados.
    """
    pedido_id = query.id
    logger.debug(f"Coletando dados sobre pedido #{pedido_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        # se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base :/"
        logger.warning(f"Erro ao buscar pedido '{pedido_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pedido econtrado: '{pedido.pedido}'")
        # retorna a representação de pedido
        return apresenta_pedido(pedido), 200


@app.delete('/pedido', tags=[pedido_tag],
            responses={"200": PedidoDelSchema, "404": ErrorSchema})
def del_pedido(query: PedidoBuscaSchema):
    """Deleta um Pedido a partir do id do pedido

    Retorna uma mensagem de confirmação da remoção.
    """
    pedido_id = query.id
    print(pedido_id)
    logger.debug(f"Deletando dados sobre pedido #{pedido_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pedido).filter(Pedido.id == pedido_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pedido #{pedido_id}")
        return {"mesage": "Pedido removido", "id": pedido_id}, 200
    else:
        # se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base :/"
        logger.warning(f"Erro ao deletar pedido #'{pedido_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.put('/pedido', tags=[pedido_tag],
         responses={"200": PedidoViewSchema, "404": ErrorSchema})
def put_pedido(query: PedidoBuscaSchema, form: PedidoAtualizaSchema):
    """Altera o status de um Pedido a partir do id do pedido

    Retorna uma representação do pedido.
    """
    pedido_id = query.id
    logger.debug(f"Alterando dados sobre pedido #{pedido_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        # se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base :/"
        logger.warning(f"Erro ao buscar pedido '{pedido_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        # alterando os dados
        pedido.status = form.status
        # mesclando a instância atualizada com a sessão e confirmando a transação
        session.merge(pedido)
        session.commit()
        logger.debug(f"Pedido econtrado: '{pedido.pedido}'")
        # retorna a representação de pedido
        return apresenta_pedido(pedido), 200


@app.get('/pedidos_por_nome', tags=[pedido_tag],
         responses={"200": PedidoViewSchema, "404": ErrorSchema})
def get_pedidos_por_nome(query: PedidoNomeBuscaSchema):
    """Faz a busca por todos os Pedidos cadastrados por nome

    Retorna uma representação da listagem de pedidos.
    """
    nome_pedido = query.pedido

    logger.debug(f"Coletando pedidos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedidos = session.query(Pedido).filter(Pedido.pedido.contains(nome_pedido)).all()

    if not pedidos:
        # se não há pedidos cadastrados
        return {"pedidos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(pedidos))
        # retorna a representação de produto
        print(pedidos)
        return apresenta_pedidos(pedidos), 200


@app.post('/menu', tags=[menu_tag],
          responses={"200": MenuViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_menu(form: MenuSchema):
    """Adiciona de um novo item ao menu de alimentos cadastrados na base identificado pelo id

    Retorna uma representação do item adicionado ao menu.
    """
    menu = Menu(
        nome_alimento = form.nome_alimento,
        cat_alimento = form.cat_alimento,
        desc_alimento = form.desc_alimento,
        preco = form.preco)

    logger.debug(f"Adicionando itens ao menu: '{menu.nome_alimento}'")
    try:
        # criando conexão com a base
        session = Session()
        # adiconando o item ao menu
        session.add(menu)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando itens ao menu: '{menu.nome_alimento}'")
        return apresenta_menu(menu), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Item de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar o item '{menu.nome_alimento}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pedido '{menu.nome_alimento}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/cardapio', tags=[menu_tag],
         responses={"200": ListagemMenuSchema, "404": ErrorSchema})
def get_cardapio():
    """Faz a busca por todos os itens cadastrados no menu

    Retorna uma representação da listagem de itens cadastrados no menu.
    """
    logger.debug(f"Listando itens no menu ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cardapio = session.query(Menu).all()

    if not cardapio:
        # se não há itens cadastrados no menu
        return {"Cardápio": []}, 200
    else:
        logger.debug(f"%d itens econtrados" % len(cardapio))
        # retorna a representação de pedido
        print(cardapio)
        return apresenta_menus(cardapio), 200