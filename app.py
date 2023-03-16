#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created: 2020-02-25
Modified: 2020-03-09
@author: abettini

Example interpolation tool. Given a function, this tool provides a (lagragian)
interpolation of the function on a uniform and Chebyshev grid defined over the
domain [a,b]. It also provides the difference between the function and the
interpolation.
"""

## Import libraries
from dash import Dash, html, dcc, Input, Output
import numpy as np
from src.interpolation import interpolation

app = Dash(__name__)
#### =========== ####
#### Application ####
#### =========== ####
app.layout = html.Div(children=[
    html.H1(children='Interpolation Unit'),

    dcc.Markdown(''' EXAMPLE LATEX:
    $$
    \\frac{1}{(\\sqrt{\\phi \\sqrt{5}}-\\phi) e^{\\frac25 \\pi}} =
    1+\\frac{e^{-2\\pi}} {1+\\frac{e^{-4\\pi}} {1+\\frac{e^{-6\\pi}}
    {1+\\frac{e^{-8\\pi}} {1+\\ldots} } } }
    $$
    EXAMPLE TEXT: \n
    LOREM LOREM LOREM
    ''',mathjax=True),

    html.Br(), html.Label('Domain: '), html.Br(),
    dcc.Input(id='a_domaininput',
              value=-4.0,
              type='number',
              placeholder='Lower Limit',
              step=0.1,
              style={'marginRight':'10px'},
             ),
    dcc.Input(id='b_domaininput',
              value=4.0,
              type='number',
              placeholder='Upper Limit',
              step=0.1
             ),
    html.Br(), html.Label('Function: '),
    html.Div(
             [dcc.Dropdown(['sign(x)', 'abs(x)', 'abs(x)^3', '1/(1+x^2)', 'exp(-x^2)', '0.001*x^5 + 0.02*x^3 - x'], '1/(1+x^2)',
                           id='f_functiondropdown',
                           searchable=False,
                          )],
             style={
                    'width': '40%'
                   }
            ),
    html.Br(), html.Label('n Slider: '),

    dcc.Slider(1, 30, 1,
               value=13,
               id='n_sliderinput',
              ),
    dcc.Graph(id='Interpolation-Graph',
              mathjax=True
             ),

])

@app.callback(Output('Interpolation-Graph','figure'),
              Input('a_domaininput','value'),
              Input('b_domaininput','value'),
              Input('n_sliderinput','value'),
              Input('f_functiondropdown','value')
             )
def update_figure(a, b, n, f_str):
    match f_str:                                      ## function to be interpolated
        case 'sign(x)':
            f = lambda x : np.sign(x)                 ## Sign function
        case 'abs(x)':
            f = lambda x : np.abs(x)                  ## C0 function
        case 'abs(x)^3':
            f = lambda x : np.abs(x)**3               ## C2 function
        case '1/(1+x^2)':
            f = lambda x : 1/(1+x**2)                 ## Cinf function (Runge function)
        case 'exp(-x^2)':
            f = lambda x : np.exp(-x**2)              ## Gaussian function
        case '0.001*x^5 + 0.02*x^3 - x':
            f = lambda x : 0.001*x**5 + 0.02*x**3 - x ## Polynomial function
        case _:
            raise NotImplementedError('Function switch-case not implemented')
    return interpolation(a, b, n, f) # function definition over a function definition ...

if __name__ == '__main__':
    app.run_server(debug=True)
