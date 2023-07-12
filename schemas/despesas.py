from pydantic import BaseModel
from typing import Optional, List
from model.despesas import Despesas

class DespesasSchema(BaseModel):
    """ Define como uma nova despesa a ser inserida deve ser representada
    """
    nome: str = "Gasolina"
    categoria: str = "Transporte"
    valor: float = 223.17
    data_despesa: str = '2023/06/02'
    comentario: Optional[str] = "43 litros"


class DespesasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da despesa.
    """
    nome: str = "Supermercado"
    categoria: str = "Casa"
    valor: float = 130.20
    data_despesa: str = '2023/06/02'
    comentario: Optional[str] = "Frutas"

class ListagemDespesasSchema(BaseModel):
    """ Define como uma listagem das despesas será retornada.
    """
    despesas:List[DespesasSchema]


def apresenta_despesas(despesas: List[Despesas]):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesaViewSchema.
    """
    result = []
    for despesa in despesas:
        result.append({
            "nome": despesa.nome,
            "categoria": despesa.categoria,
            "valor": despesa.valor,
            "data_despesa": despesa.data_despesa,
            "comentario": despesa.comentario,
        })

    return {"despesas": result}


class DespesasViewSchema(BaseModel):
    """ Define como uma despesa será retornada: despesa.
    """
    id: int = 1
    nome: str = "Gasolina"
    categoria: str = "Transporte"
    valor: float = 223.17
    data_despesa: str = '20230602'
    comentario: str = "43 litros"

class DespesasDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_despesa(despesas: Despesas):
    """ Retorna uma representação da despesa seguindo o schema definido em
        DespesasViewSchema.
    """
    return {
        "id": despesas.id,
        "nome": despesas.nome,
        "categoria": despesas.categoria,
        "valor": despesas.valor,
        "data_despesa": despesas.data_despesa,
        "comentario": despesas.comentario
    }
