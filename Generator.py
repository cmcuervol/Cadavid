# -*- coding: utf-8 -*-

import numpy as np
import datetime as dt
import pandas as pd


def MakeTable(Trans, Hechos, Clientes, Origenes, Destinos, F_ini='2018-5-1', F_fin='2018-5-31'):
    """
    Make an aleatory table with the parametrized quantities
    INPUTS
    Trans: quantity of transactions
    HC   : integers of Hechos contables
    """
    start = dt.datetime.strptime(F_ini, '%Y-%m-%d')
    end   = dt.datetime.strptime(F_fin, '%Y-%m-%d')
    day   = (end-start).days+1

    T  = np.random.randint(1,100,      size=Trans)
    Hc = np.random.randint(1,Hechos,   size=Trans)
    C  = np.random.randint(1,Clientes, size=Trans)
    F  = np.random.randint(0,day,      size=Trans)
    O  = np.random.randint(0,Origenes, size=Trans)
    D  = np.random.randint(0,Destinos, size=Trans)

    fec = [start+dt.timedelta(days=int(F[i])) for i in range(Trans)]

    Table = pd.DataFrame(np.array([Hc,fec,C, O, D, T]).T, columns=['Id_Hecho_Contable', 'Fecha_Movimiento_Contable', 'Id_Cliente', 'Id_Cuenta_Origen', 'Id_Cuenta_Destino', 'Valor ($)'])

    return Table

Trans = 100
Clientes = 4
Hechos = 5
F_ini = '2018-5-1'
F_fin = '2018-5-31'
Origenes = 10
Destinos = 10

Tabla = MakeTable(Trans, Hechos, Clientes, Origenes, Destinos, F_ini='2018-5-1', F_fin='2018-5-31')

Ord = Tabla.sort_values(['Id_Hecho_Contable', 'Fecha_Movimiento_Contable', 'Id_Cliente'], ascending=[True, True, True])










print("Hello world")
