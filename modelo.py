#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Altas, Bajas y Modificaciones
"""

import sqlite3
conn = sqlite3.connect('./registroHorario.db')
ejecutor = conn.cursor()


class ErrorDeMultiplesValores(Exception):
    print("Ha ocurrido un error que se puede deber a:\n\t*\tintentar asignar varios valores en una clausula que admite solo uno (ej.:UPDATE)")


def seleccion(query):
    consulta = ejecutor.execute(query)
    return list(consulta)

def operacionDirecta(query):
    try:
        ejecutor.execute(query)
    except Exception as e:
        print(e)


def operacionSimple(tipo,tabla,campos,valores,clausulaWhere=None):
    """
    operaciones simples de base de datos

    :param tipo: A (alta) B (Baja) M (Modificacion)
    :param tabla: string. tabla en la que operamos
    :param clausulaWhere: string. Condicion que sigue al ´WHERE
    :return:
    """
    query = ""
    if tipo == "A":
        query = "INSERT INTO %s (%s) VALUES (%s)"%(tabla,campos,valores)
    if tipo == "B":
        query = "DELETE FROM %s"%tabla
    if tipo == "M":
        query = "UPDATE %s SET %s = %s" % (tabla, campos, valores)


    if clausulaWhere != None:
        query += " WHERE %s"%clausulaWhere

    try:
        consulta = ejecutor.execute(query)
        conn.commit()
        print("Exito!")
    except Exception as e:
        print("Error al intentar operar.")
        print(e)


#if __name__ == '__main__':
    #operacionSimple("A","Asistencia"," 'dia','mes','anio','horaIngreso','minutoIngreso','horaEgreso','minutoEgreso','Feriado','Almuerzo' ", " 5,3,2019,8,1,null,null,1,1 " )
    #operacionSimple("M","Asistencia","MinutoEgreso",10," ID = 8")










