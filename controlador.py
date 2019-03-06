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
    try:
        # Conseguir la marca . Revisando la marca del ultimo registro
        inicioRotacion = 1
        ultimoTipoMarca = seleccion(" SELECT ID FROM  tipoMarca ORDER BY ID DESC LIMIT 1")[0][0]
        ultimaMarca = seleccion(" SELECT marca_FK FROM  Asistencias ORDER BY jornada_FK DESC LIMIT 1")[0][0]
        marca = (ultimaMarca % ultimoTipoMarca) + inicioRotacion

        # consigue el tiempo actual
        temp = getTiempo()
        fechaActual = temp[:3]
        horaMinutoActual = temp[-2:]

        #Consigue la jornada
        # comparar el tiempo obtenido con la maquina con el de la ultima jornada existente (si no existe se crea)
        ultimaJornada = seleccion("SELECT dia,mes,anio FROM jornadas ORDER BY ID DESC LIMIT 1")[0]
        if fechaActual == list(ultimaJornada):
            IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s"%ultimaJornada)[0][0]
        else:
            # se analiza la jornada previa
            #calculoJornadaPrevia()
            # se crea la jornada

            IDjor = operacionSimple("A","jornadas"," 'dia', 'mes', 'anio' ", " %s, %s , %s "%tuple(fechaActual))
            # La siguiente busqueda tambien puede ser por ultimo valor de jornadas
            IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s" %tuple(fechaActual))[0][0]

        #Marca asistencia
        operacionSimple("A","Asistencias","  'jornada_FK', 'hora', 'minuto', 'marca_FK' "," %s, %s, %s, %s" %(IDjor,horaMinutoActual[0],horaMinutoActual[1],marca) )
        return "Marcacion Exitosa!"

    except Exception as e:
        return "Fallo en el proceso de Marcado :-("

def calculoJornadaPrevia():
    jornadaPrevia = seleccion("SELECT * from jornadas order by ID desc limit 1")[0]
    registrosEntrada = seleccion("SELECT * FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(jornadaPrevia[0],1))
    registrosSalida = seleccion("SELECT * FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(jornadaPrevia[0],2))
    print(registrosEntrada)
    print(registrosSalida)
    if len(registrosEntrada) != len(registrosSalida):
        raise NameError("La cantidad de entradas y salidas son inconsistentes, arregle el problema manualmente")
    else:
        pass










if __name__ == '__main__':
    conectar()
    print(marcar())
    """
    conectar()
    print(calculoJornadaPrevia())
    """

"""
Hacer Marcaciones 
    
"""











