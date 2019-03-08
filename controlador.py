#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *

# aquí van variables globales que integrar a la BD sería innecesario debido a que son pocos los casos
horasNecesariasPresentismo = 7

def getTiempo():
    from datetime import datetime
    tiempo = datetime.now()
    return [tiempo.day,tiempo.month,tiempo.year,tiempo.hour,tiempo.minute]

def diferenciaHoras(p_marca1,p_marca2):
    # toma si o si dia mes y año
    from datetime import datetime

    if len(p_marca1) == len(p_marca2) == 5:
        marca1 = datetime.strptime("%s %s %s %s %s"%tuple(p_marca1),"%d %m %Y %H %M")
        marca2 = datetime.strptime("%s %s %s %s %s"%tuple(p_marca2),"%d %m %Y %H %M")
        lapso = marca2 - marca1
        return lapso
    if len(p_marca1) == len(p_marca2) == 2:
        marca1 = datetime.strptime("%s %s" % tuple(p_marca1), "%H %M")
        marca2 = datetime.strptime("%s %s" % tuple(p_marca2), "%H %M")
        lapso = marca2 - marca1
        return lapso
    raise NameError('Error en la cantidad de parametros de fechas a sustraer (5 o 3) ningun otro valor.')


def marcar():
    try:
        # Conseguir la marca . Revisando la marca del ultimo registro
        inicioRotacion = 1
        ultimoTipoMarca = seleccion(" SELECT ID FROM  tipoMarca ORDER BY ID DESC LIMIT 1")[0][0]
        ultimaMarca = seleccion(" SELECT marca_FK FROM  Asistencias ORDER BY jornada_FK DESC, ID DESC  LIMIT 1")[0][0]
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
            jornadaPrevia = seleccion("SELECT ID from jornadas order by ID desc limit 1")[0][0]
            calculoJornada(jornadaPrevia)
            return None
            # se crea la jornada
            operacionSimple("A","jornadas"," 'dia', 'mes', 'anio', 'tipoJornada_FK' ", " %s, %s , %s, 1 "%tuple(fechaActual))
            # La siguiente busqueda tambien puede ser por ultimo valor de jornadas
            IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s" %tuple(fechaActual))[0][0]

        #Marca asistencia
        operacionSimple("A","Asistencias","  'jornada_FK', 'hora', 'minuto', 'marca_FK' "," %s, %s, %s, %s" %(IDjor,horaMinutoActual[0],horaMinutoActual[1],marca) )
        return "Marcacion Exitosa!"

    except Exception as e:
        print(e)
        return "Fallo en el proceso de Marcado :-("


def calculoJornada(IDjor):
        presentismo = False
        horasDemas = 0
        mesJornada = seleccion("select mes from jornadas WHERE ID = 10")[0][0]
        registrosEntrada = seleccion("SELECT jornada_FK,HORA,MINUTO FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(IDjor,1))
        registrosSalida = seleccion("SELECT jornada_FK,HORA,MINUTO FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(IDjor,2))

        if len(registrosEntrada) != len(registrosSalida):
            raise NameError("La cantidad de entradas y salidas son inconsistentes, arregle el problema manualmente")
        else:
           for x,y in  zip(registrosEntrada,registrosSalida):
               # calculo de presentismo
               if not presentismo:
                   dif = diferenciaHoras(x[1:], y[1:])
                   if dif.seconds//3600 > horasNecesariasPresentismo:
                       totalhoras = seleccion(" SELECT totalHoras FROM Conceptos WHERE mes = %i and tipoConcepto_FK = 1"%mesJornada)[0][0]
                       operacionSimple("M","Conceptos","totalHoras",totalhoras+horasNecesariasPresentismo,"mes = 3 and tipoConcepto_FK = 1")
                       presentismo = True
               else:
                   pass
                   # se calculan horas extra al 50 o al 100





if __name__ == '__main__':
    conectar()
    print(calculoJornada(10))














