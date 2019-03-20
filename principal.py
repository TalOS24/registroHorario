#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import conectar
from tareasMantenimiento import *
from controlador import *


if __name__ == '__main__':
    conectar()
    print("------ Principal -----------")
    #print(calculoPeriodo_ImpactoBD([20,3,2019],getTiempo()[:3]))
    print(ficharAlmuerzo(12))
    #print(marcacion())