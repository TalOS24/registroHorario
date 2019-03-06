#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *


def getTiempo():
    from datetime import datetime
    tiempo = datetime.now()
    return [tiempo.day,tiempo.month,tiempo.year,tiempo.hour,tiempo.minute]

def diferenciaHoras(p_marca1,p_marca2):
    from datetime import datetime
    marca1 = datetime.strptime("%s %s %s %s %s"%tuple(p_marca1),"%d %m %Y %H %M")
    marca2 = datetime.strptime("%s %s %s %s %s"%tuple(p_marca2),"%d %m %Y %H %M")
    lapso = marca2 - marca1
    return lapso

def marcar():

    # Revisa la marca del ultimo registro
    inicioRotacion = 1
    ultimoTipoMarca = seleccion(" SELECT ID FROM  tipoMarca ORDER BY ID DESC LIMIT 1")[0][0]
    ultimaMarca = seleccion(" SELECT marca_FK FROM  Asistencias ORDER BY jornada_FK DESC LIMIT 1")[0][0]
    marca = (ultimaMarca % ultimoTipoMarca) + inicioRotacion

    # consigue el tiempo actual

    temp = getTiempo()
    fechaActual = temp[:3]
    horaMinutoActual = temp[-2:]

    # TODO: si no existe la jornada crearla
        # comparar el tiempo obtenido con la maquina con el de la ultima jornada existente (si no existe se crea)
    ultimaJornada = seleccion("SELECT dia,mes,anio FROM jornadas ORDER BY ID DESC LIMIT 1")[0]
    ultimaJornada = (3,3,2019) # prueba
    if fechaActual == list(ultimaJornada):
        IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s"%ultimaJornada)[0][0]
    else:
        # se crea la jornada
        IDjor = operacionSimple("A","jornadas"," 'dia', 'mes', 'anio' ", " %s, %s , %s "%tuple(fechaActual))
        IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s" %tuple(fechaActual))[0][0]
        print(IDjor)



if __name__ == '__main__':
    conectar()
    marcar()








