#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *
from controlador import *

def generarConceptosMensuales(excepciones=[]):
    #Capturar tipos de concepto
    identificadores  = seleccion("select id from tipoConcepto order by id DESC ")
    identificadores = enlistar(identificadores)

    # obtener la fecha actual
    fechaActual = getTiempo()[:3]

    #TODO: insertar los registros dentro de la tabla concepto

    return identificadores #"Termino de generar conceptos mensuales"




def backup():
    # Por ahora en txt
    # Resguardo de asistencias
    filas = seleccion("select * from Asistencias")
    with open("backups.txt","w") as arch:
        for fila in filas:
            arch.write(str(fila)+"\n")
    arch.close()




    #return "Terminaron las tareas de mantenimiento"


