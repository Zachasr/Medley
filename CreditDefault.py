# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 13:31:47 2022

@author: Alexis.Vivien

Naive modeling of credite defaults using a Markov Random Field
http://webia.lip6.fr/~phw/aGrUM/docs/current/notebooks/NaiveCreditDefaultModeling.ipynb.html
"""

import numpy as np
import matplotlib.pyplot as plt

import pyAgrum as gum
import pyAgrum.lib.notebook as gnb
import pyAgrum.lib.mn2graph as m2g
import errno

# building nodes (with types)
mn = gum.MarkovNet('Credit default modeling')

# Adding sector variables
sectors = ['Finance', 'Energy', 'Retail']
finance, energy, retail = [mn.add(gum.LabelizedVariable(name, '', ['no stress', 'under stress'])) 
                           for name in sectors]

# Adding issuer variables
mb, db, ba = [mn.add(gum.LabelizedVariable(name, '', ['no default', 'default'])) 
              for name in ['Metro Bank', 'Deutsche Bank', 'Barclays']]

edf, petro, eq = [mn.add(gum.LabelizedVariable(name, '', ['no default', 'default'])) 
              for name in ['EDF','Petrobras','EnQuest']]

nl, matalan, ms = [mn.add(gum.LabelizedVariable(name, '', ['no default', 'default'])) 
              for name in ['New Look', 'Matalan', 'Marks & Spencer']]
# Adding and filling factors between sectors
mn.addFactor([finance, energy])[:] = [[90, 70],
                                      [60, 10]]
mn.addFactor([finance, retail])[:] = [[80, 10],
                                      [30, 80]]
mn.addFactor([energy, retail])[:]  = [[60,  5],
                                      [70, 95]]

# Adding factors between sector and issuer
mn.addFactor([db, finance])[:] = [[90, 30],
                                  [10, 60]]
mn.addFactor([mb, finance])[:] = [[80, 40],
                                  [ 5, 60]]
mn.addFactor([ba, finance])[:] = [[90, 20],
                                  [20, 50]]

mn.addFactor([edf, energy])[:]   = [[90, 5],
                                    [80, 40]]
mn.addFactor([petro, energy])[:] = [[60, 50],
                                    [ 5, 60]]
mn.addFactor([eq, energy])[:]    = [[80, 20],
                                    [10, 50]]


mn.addFactor([nl, retail])[:]      = [[ 5, 60],
                                      [ 2, 90]]
mn.addFactor([matalan, retail])[:] = [[40, 30],
                                      [20, 70]]
mn.addFactor([ms, retail])[:]       = [[80, 10],
                                      [30, 50]]
nodetypes={n:0.1 if n in sectors else 
             0.2 for n in mn.names()}

gnb.sideBySide(gnb.getMN(mn,view='graph',nodeColor=nodetypes),
               gnb.getMN(mn,view='factorgraph',nodeColor=nodetypes),
              captions=['The model as a Markov Network','The model as a factor graph'])

gnb.sideBySide(mn.factor({'Energy', 'Finance'}),
               mn.factor({'Finance', 'Retail'}),
               mn.factor({'Energy', 'Retail'}))

gnb.sideBySide(mn.factor({'Deutsche Bank', 'Finance'}),
               mn.factor({'Metro Bank', 'Finance'}),
               mn.factor({'Barclays', 'Finance'}))

gnb.sideBySide(mn.factor({'EDF', 'Energy'}),
               mn.factor({'Petrobras', 'Energy'}),
               mn.factor({'EnQuest', 'Energy'}))

gnb.sideBySide(mn.factor({'New Look', 'Retail'}),
               mn.factor({'Matalan', 'Retail'}),
               mn.factor({'Marks & Spencer', 'Retail'}))

