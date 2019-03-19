#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import seleccion,operacionSimple


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

def marcacion(hora=None,minuto=None):
    try:
        # Consigue la marca . Revisando la marca del ultimo registro
        inicioRotacion = 1
        ultimoTipoMarca = seleccion(" SELECT ID FROM  tipoMarca ORDER BY ID DESC LIMIT 1")[0][0]
        ultimaMarca = seleccion(" SELECT marca_FK FROM  Asistencias ORDER BY jornada_FK DESC, ID DESC  LIMIT 1")[0][0]
        marca = (ultimaMarca % ultimoTipoMarca) + inicioRotacion
        # consigue el tiempo actual
        temp = getTiempo()
        fechaActual = temp[:3]
        # analiza si es diferida o exacta
        if hora != None and minuto != None:
            horaMinuto = [hora,minuto]
        else:
            horaMinuto = temp[-2:]

        #Consigue la jornada
        ultimaJornada = seleccion("SELECT dia,mes,anio FROM jornadas ORDER BY ID DESC LIMIT 1")[0]
        if fechaActual == list(ultimaJornada):
            IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s"%ultimaJornada)[0][0]
        else:
            # se crea la jornada
            operacionSimple("A","jornadas"," 'dia', 'mes', 'anio', 'tipoJornada_FK' ", " %s, %s , %s, 1 "%tuple(fechaActual))
            # La siguiente busqueda tambien puede ser por ultimo valor de jornadas
            IDjor = seleccion("SELECT ID FROM jornadas WHERE DIA=%s AND MES=%s AND ANIO=%s" %tuple(fechaActual))[0][0]
        #Marca asistencia
        operacionSimple("A","Asistencias","  'jornada_FK', 'hora', 'minuto', 'marca_FK' "," %s, %s, %s, %s" %(IDjor,horaMinuto[0],horaMinuto[1],marca) )
        return "Marcacion Exitosa!"

    except Exception as e:
        print(e)
        return "Fallo en el proceso de Marcado :-("

def calculoJornada_ImpactoBD(IDjor):
        presentismo = False
        horasDemas = 0
        mesJornada,anioJornada = seleccion("select mes,anio from jornadas WHERE ID = %i"%IDjor)[0]
        registrosEntrada = seleccion("SELECT jornada_FK,HORA,MINUTO FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(IDjor,1))
        registrosSalida = seleccion("SELECT jornada_FK,HORA,MINUTO FROM asistencias WHERE jornada_FK = %i and marca_FK = %i"%(IDjor,2))

        if len(registrosEntrada) != len(registrosSalida):
            raise NameError("La cantidad de entradas y salidas son inconsistentes, arregle el problema manualmente")
        else:
            for x,y in  zip(registrosEntrada,registrosSalida):
                dif = diferenciaHoras(x[1:], y[1:])
                dif = dif.seconds / 3600

               # calculo de presentismo
                if not presentismo:
                    id_tipoConcepto = seleccion("select ID from tipoConcepto where descripcion like '%Presentismo%' ")[0][0]
                    if dif > horasNecesariasPresentismo:
                        totalhoras = seleccion("SELECT totalHoras FROM Conceptos WHERE mes = %i and anio=%i and tipoConcepto_FK = %i"%(mesJornada,anioJornada,id_tipoConcepto))[0][0]
                        operacionSimple("M","Conceptos","totalHoras",totalhoras+horasNecesariasPresentismo,"mes = %i and anio=%i and tipoConcepto_FK = %i"%(mesJornada,anioJornada,id_tipoConcepto))
                        presentismo = True
                        horasDemas += dif - 7
                    else:
                        horasDemas += dif

            # ya calculadas las horas demas resta verificar si la jornada es extra al 50% o al 100%
            tipoJornada = seleccion("Select tipoJornada.ID,tipoJornada.descripcion from jornadas INNER JOIN tipoJornada ON jornadas.tipoJornada_FK = tipoJornada.ID where jornadas.ID = %i"%IDjor)[0]
            if tipoJornada[1] == "regular" or tipoJornada[1]== "extra %50":
                id_tipoConcepto = seleccion("select ID from tipoConcepto where descripcion like '%50%' ")[0][0]
                #print("jornada regular")

            if tipoJornada[1] == "extra %100":
                id_tipoConcepto = seleccion("select ID from tipoConcepto where descripcion like '%100%' ")[0][0]
                #print("jornada feriado")

            # Ahora se calcula e impacta en BD
            id_concepto = seleccion(
                "select Conceptos.ID from Conceptos where Conceptos.tipoConcepto_FK = %i and Conceptos.mes = %i and Conceptos.anio = %i" % (
                    id_tipoConcepto, mesJornada, anioJornada))[0][0]
            horasExistentes = seleccion("select totalHoras from conceptos where ID = %i" % id_concepto)[0][0]
            horasExistentes += horasDemas
            operacionSimple("M", "Conceptos", "totalHoras", horasExistentes,
                            "mes = %i and anio=%i and tipoConcepto_FK = %i" % (
                                mesJornada, anioJornada, id_tipoConcepto))
        return "Exito: Jornada Calculada"

# p_ inicio ejemplo: [1,1,1991] = 1 de enero de 1991
def calculoPeriodo_ImpactoBD(p_inicio,p_fin):
    inicioJor = seleccion("select id from jornadas where dia = %i and mes = %i and anio= %i"%tuple(p_inicio))[0][0]
    finJor=seleccion("select id from jornadas where dia = %i and mes = %i and anio= %i"%tuple(p_fin))[0][0]
    id_jornadas = seleccion("select id from jornadas where id between %i and %i"%(inicioJor,finJor))
    id_jornadas = [x[0] for x in id_jornadas]
    for id in id_jornadas:
        calculoJornada_ImpactoBD(id)
    return "Exito: Periodo calculado"

















