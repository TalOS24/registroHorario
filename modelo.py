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
    except NameError as variable_vacia:
        print("Usted debe conectar a la base de datos. Por favor use para ello la función conectar() antes de llamar a esta seleccion()")
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
        print("su consulta es:\n\t%s"%query)
        print(e)

def enlistar(lista):
    """
    Toma valores de las consultas y los transforma en listas.
    El unico caso en el que esto tiene sentido es si la consulta devuelve un único valor
    :param lista: lista de elementos extraídos de la BD
    :return: lista de un solo nivel
    """
    respuesta = [x[0] for x in lista]
    return respuesta


















