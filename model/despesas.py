from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Despesas(Base):
    __tablename__ = 'despesas'

    id = Column("pk_id", Integer, primary_key=True)
    nome = Column(String(40))
    categoria = Column(String(20))
    valor = Column(Float)
    data_despesa = Column(String(8))
    comentario = Column(String(40))

    def __init__(self, nome:str, categoria:str, valor:float,
                 data_despesa:str,comentario:str):
        """
        Cria uma Despesa

        Arguments:
            nome: nome da despesa efetuada.
            categoria: categoria da despesa
            valor: valor da despesa
            data_depesa: data de quando a despesa foi efetuada
            comentario: comentário descrevendo informação sobre a despesa
        """
        self.nome = nome
        self.categoria = categoria
        self.valor = valor
        self.data_despesa = data_despesa
        self.comentario = comentario


