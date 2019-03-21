#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *


def generarConceptosMensuales(excepciones=[]):
    #Capturar ultimo tipo de concepto creado
    #TODO: Aquí tambien se podría verificar si se elimino algún concepto
    id_ultimo_concepto = seleccion("select id from tipoConcepto order by id DESC ")
    print(id_ultimo_concepto)

    """    
    Falta hacer un bucle for que recorra desde 1 hasta ultimo concepto
    luego generar los conceptos en la tabla
    """

    return "Termino de generar conceptos mensuales"




def backup():
    # Por ahora en txt
    # Resguardo de asistencias
    filas = seleccion("select * from Asistencias")
    with open("backups.txt","w") as arch:
        for fila in filas:
            arch.write(str(fila)+"\n")
    arch.close()




    #return "Terminaron las tareas de mantenimiento"


