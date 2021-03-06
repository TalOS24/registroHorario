#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *
from controlador import *

def generarConceptosMensuales(excepciones=[]):
    """
    Esta función se debe correr al principio de mes.
    No se hacen validaciones (por ejemplo comprobar si ya se corrio este programa) porque
    esto no es una función a la que accedera el usuario.
    :param excepciones:
    :return:
    """
    #Capturar tipos de concepto
    identificadores  = seleccion("select id from tipoConcepto")
    identificadores = enlistar(identificadores)
    # obtener la fecha actual
    fechaActual = getTiempo()[1:3]
    # impactar en BD
    for ident in identificadores:
        valores =  "%i,%i,%i,%f"%(*fechaActual,ident,0.0)
        operacionSimple("A","Conceptos","mes,anio,tipoConcepto_FK,totalHoras",valores)
    return "Termino de generar conceptos mensuales"


def backup_manual_asistencias(p_nombre,formato="txt"):
    # Por ahora en txt
    # Resguardo de asistencias
    filas = seleccion("select * from Asistencias")
    with open("%s.txt"%p_nombre,"w") as arch:
        for fila in filas:
            arch.write(str(fila)+"\n")
    arch.close()

def restore_manual_asistencias():
    pass
    # toma por ahora del txt
    # Restauración que impacta en BD.
    # return "Terminaron las tareas de mantenimiento"

if __name__ == '__main__':
    conectar()
    backup_manual_asistencias("backup")








