#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Altas, Bajas y Modificaciones
"""
def conectar():
    global conn
    global ejecutor
    import sqlite3
    conn = sqlite3.connect('./registroHorario.db')
    ejecutor = conn.cursor()

def seleccion(query):
    try:
        consulta = ejecutor.execute(query)
    except Exception as e:
        print("Error en el select")
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
        #print("Operacion realizada con exito! confimado impacto en Base de datos")
    except Exception as e:
        print("Error al intentar operar.")
        print(e)



"""
if __name__ == '__main__':
    conectar()
    print(seleccion("select * from CalendarioMeses"))
"""
















