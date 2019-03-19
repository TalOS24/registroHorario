#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import *

def backup():
    # Por ahora en txt
    # Resguardo de asistencias
    filas = seleccion("select * from Asistencias")
    with open("backups.txt","w") as arch:
        for fila in filas:
            arch.write(str(fila)+"\n")
    arch.close()

def almuerzos():
    #for i in range (9):
    operacionSimple("M","jornadas", " 'eventos' ", " 1 ")
    #return "Terminaron las tareas de mantenimiento"


