#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modelo import operacionSimple


# TODO: Construir función que reste horas entre si de manera tal que se pueda calcular tiempo entre marcaciones.
# TODO: construir función que permita la marcación en el momento que se la llama

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


if __name__ == '__main__':
    print((diferenciaHoras([5,3,2019,8,15],[5,3,2019,16,25])))







