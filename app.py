from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Despesas
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Despesa API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
despesa_tag = Tag(name="Despesa", description="Adição, visualização e remoção de despesas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cadastrar_despesa', tags=[despesa_tag],
          responses={"200": DespesasViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_despesa(form: DespesasSchema):
    """Adiciona uma nova despesa à base de dados

    Retorna uma representação das despesas
    """
    despesa = Despesas(
        nome=form.nome,
        categoria=form.categoria,
        valor=form.valor,
        data_despesa=form.data_despesa,
        comentario=form.comentario)
    logger.debug(f"Adicionando despesa: '{despesa.nome}'")
    print('data despesa', despesa.data_despesa)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(despesa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado despesa: '{despesa.nome}'")
        return apresenta_despesa(despesa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Despesa de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar despesa '{despesa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/buscar_despesa', tags=[despesa_tag],
         responses={"200": ListagemDespesasSchema, "404": ErrorSchema})
def get_despesas():
    """Faz a busca por todas as despesas cadastradas

    Retorna uma representação da listagem de despesas.
    """
    logger.debug(f"Coletando despesas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    despesas = session.query(Despesas).all()
    if not despesas:
        # se não há despesas cadastradas
        return {"despesas": []}, 200
    else:
        logger.debug(f"%d despesas econtradas" % len(despesas))
        # retorna a representação da despesa
        print(despesas)
        return apresenta_despesas(despesas), 200

@app.delete('/deletar_despesa', tags=[despesa_tag],
            responses={"200": DespesasSchema, "404": ErrorSchema})
def del_despesa(query: DespesasBuscaSchema):
    """Exclui uma despesa a partir do nome da despesa informada

    Retorna uma mensagem de confirmação da remoção.
    """
    despesa_nome = unquote(unquote(query.nome))
    despesa_categoria = unquote(unquote(query.categoria))
    despesa_valor = query.valor
    despesa_data_despesa = query.data_despesa
    logger.debug(f"Deletando dados sobre a despesa #{despesa_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Despesas).filter(Despesas.nome == despesa_nome, Despesas.categoria == despesa_categoria, \
                        Despesas.valor == despesa_valor).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada despesa #{despesa_nome}")
        return {"mesage": "Despesa removida", "id": despesa_nome}
    else:
        # se a despesa não foi encontrada
        error_msg = "Despesa não encontrada na base :/"
        logger.warning(f"Erro ao deletar despesa {despesa_nome}', {error_msg}")
        return {"mesage": error_msg}, 404



