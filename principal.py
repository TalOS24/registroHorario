#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import conectar
from controlador import *


if __name__ == '__main__':
    conectar()
    print("------ Principal -----------")
    print(calculoPeriodo_ImpactoBD())
    print(marcacion())