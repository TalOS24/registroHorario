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



"""
if __name__ == '__main__':
    conectar()
 
"""

