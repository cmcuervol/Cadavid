# -*- coding: utf-8 -*-

import numpy as np
import datetime as dt
import pandas as pd
import argparse
import sys, os

Path = os.path.abspath(os.path.dirname(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--transferencias", default=1000,       help="quantity of transactions")
parser.add_argument("-c", "--clientes",       default=200,        help="clients quantity")
parser.add_argument("-e", "--hechos",         default=10,         help="Hechos contables quantity")
parser.add_argument("-i", "--inicio",         default='2018-5-1', help="initial date in format ''%Y-%m-%d' example '2018-05-01'")
parser.add_argument("-f", "--final",          default='2018-5-31',help="final date in format ''%Y-%m-%d' example '2018-05-31'")
parser.add_argument("-o", "--origenes",       default=10,         help="sources quantity")
parser.add_argument("-d", "--destinos",       default=10,         help="destinations quantity")
args = parser.parse_args()

Trans    = int(args.transferencias)
Clientes = int(args.clientes)
Hechos   = int(args.hechos)
F_ini    = str(args.inicio)
F_fin    = str(args.final)
Origenes = int(args.origenes)
Destinos = int(args.destinos)

def MakeTable(Trans, Hechos, Clientes, Origenes, Destinos, F_ini='2018-05-01', F_fin='2018-05-31'):
    """
    Make an aleatory table with the parametrized quantities
    INPUTS
    Trans    : quantity of transactions
    Hechos   : integers of Hechos contables quantity
    Clientes : integer of clients quantity
    Origenes : integer of sources quantity
    Destinos : integet of destinations quantity
    F_ini    : initial date in format ''%Y-%m-%d' example '2018-05-01'
    F_fin    : final date in format ''%Y-%m-%d' example '2018-05-31'
    OUTPUTS
    Table:  Table with the random values sorted by the three initial columns
    """
    start = dt.datetime.strptime(F_ini, '%Y-%m-%d')
    end   = dt.datetime.strptime(F_fin, '%Y-%m-%d')
    day   = (end-start).days+1

    T  = np.random.randint(1,100,      size=Trans)
    Hc = np.random.randint(1,Hechos+1,   size=Trans)
    C  = np.random.randint(1,Clientes+1, size=Trans)
    F  = np.random.randint(0,day,      size=Trans)
    O  = np.random.randint(1,Origenes+1, size=Trans)
    D  = np.random.randint(1,Destinos+1, size=Trans)

    fec = [start+dt.timedelta(days=int(F[i])) for i in range(Trans)]

    Table = pd.DataFrame(np.array([Hc,fec,C, O, D, T]).T, columns=['Id_Hecho_Contable', 'Fecha_Movimiento_Contable', 'Id_Cliente', 'Id_Cuenta_Origen', 'Id_Cuenta_Destino', 'Valor ($)'])

    Table = Table.sort_values(['Id_Hecho_Contable', 'Fecha_Movimiento_Contable', 'Id_Cliente'], ascending=[True, True, True])
    Table.index = np.arange(Trans)
    return Table



Tabla = MakeTable(Trans, Hechos, Clientes, Origenes, Destinos, F_ini='2018-5-1', F_fin='2018-5-31')


M = np.zeros((Trans, Origenes, Destinos), dtype=float)
C = np.zeros((Trans, Origenes))
D = np.zeros((Trans, Destinos))
for i in range(Trans):
    id_orig = Tabla['Id_Cuenta_Origen'] [i] -1
    id_dest = Tabla['Id_Cuenta_Destino'][i] -1

    M[i,id_orig,id_dest] = Tabla['Valor ($)'][i]

    C[i,:] = np.sum(M[i], axis=1)
    D[i,:] = np.sum(M[i], axis=0)

Tablazo = []
for i in range(Trans):
    Line = [Tabla['Fecha_Movimiento_Contable'][i], Tabla['Id_Cliente'][i], Tabla['Id_Hecho_Contable'][i], M[i], C[i],D[i]]

    if i == 0:
        delta = 0
    elif (Tabla['Fecha_Movimiento_Contable'][i-delta-1] == Tabla['Fecha_Movimiento_Contable'][i])\
       & (Tabla['Id_Hecho_Contable'][i-delta-1]         == Tabla['Id_Hecho_Contable'][i])\
       & (Tabla['Id_Cliente'][i-delta-1]                == Tabla['Id_Cliente'][i]):
        delta +=1
        # print("entré ", i)
        continue

    if delta >0:
        M_acum = np.sum(M[i-delta:i], axis=0)+M[i]
        C_acum = np.sum(C[i-delta:i], axis=0)+C[i]
        D_acum = np.sum(D[i-delta:i], axis=0)+D[i]

        Line = [Tabla['Fecha_Movimiento_Contable'][i], Tabla['Id_Cliente'][i], Tabla['Id_Hecho_Contable'][i], M_acum, C_acum,D_acum]
        # print('parchado', i)
        delta = 0

    Tablazo.append(Line)



x = []
for i in range(Trans):
    x.append(u"INSERT INTO tesis.FCT_Movimiento_Contable values ("\
             +str(Tabla.iloc[i,0])+","\
             +"'"+Tabla.iloc[i,1].strftime('%Y-%m-%d')+"',"\
             +str(Tabla.iloc[i,2])+","\
             +str(Tabla.iloc[i,3])+","\
             +str(Tabla.iloc[i,4])+","\
             +str(Tabla.iloc[i,5])+");"\
            )
a = open (os.path.join(Path,'Original.txt'), 'w')
a.writelines( "%s\n" % str(item) for item in x )
a.close()



X = []
for i in range(len(Tablazo)):
    Matriz = ''
    for j in range(Origenes):
        Matriz += 'array('
        for k in range(Destinos):
            Matriz += str(Tablazo[i][3][j,k])
            if k <Destinos-1:
                Matriz += ","
        Matriz += ")"
        if j < Origenes-1:
            Matriz += ','
    X.append(u"INSERT INTO tesis.FCT_Movimiento_Contable_MAT select "\
             + str(i)+",'"+ Tablazo[i][0].strftime('%Y-%m-%d') + "',"\
             + str(Tablazo[i][1]) + ","\
             + str(Tablazo[i][2]) + ", array("\
             + Matriz + ") from dummy;"
            )

b = open (os.path.join(Path,'Modificado.txt'), 'w')
b.writelines( "%s\n" % str(item) for item in X )
b.close()


print("Hello world")
