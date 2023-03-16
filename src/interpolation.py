
import numpy as np
import scipy.interpolate as interpolate
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def interpolation(a, b, n, f):
    if b > a:
        L = [a,b]                           ## Domain
    else:
        raise ValueError('Domain endpoints incorrectly defined: a > b')

    #### ========= ####
    #### Main Code ####
    #### ========= ####
    x_test            = np.linspace(L[0],L[1],1000)         ## Points used to evaluate function and interpolant to create plots

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=('Linear Grid', 'Chebyshev-Gauss Grid', 'Interpolation Difference')
                       )

    #### ================= ####
    #### Main Calculations ####
    #### ================= ####
    i               = np.arange(1,n+1,1)
    ## Local grid generation
    xi_linear       = np.linspace(-1,1,n) if n != 1 else np.asarray( [0] )  # Rare edge-case when n = 1 -> linear grid takes an endpoint, whereas the chebyshev grid case gets the midpoint
    xi_chebyshev    = np.cos( (2*i - 1)/(2*n)*np.pi )   # Zeros of T_n
    ## Grid transformation
    x_linear        = (L[1]+L[0])/2 + (L[1]-L[0])/2*xi_linear  # np.linspace(L[0],L[1],n) achieves the same thing
    x_chebyshev     = (L[1]+L[0])/2 + (L[1]-L[0])/2*xi_chebyshev
    ## f evaluation
    f_linear        = f(x_linear)
    f_chebyshev     = f(x_chebyshev)
    ## Interpolation
    poly_linear     = interpolate.lagrange(x_linear,f_linear)
    poly_chebyshev  = interpolate.lagrange(x_chebyshev,f_chebyshev) # Does not matter what kind of interpolation method used -> leads to same polynomial, polynomial is grid-dependent, not method-dependent

    #### ================== ####
    #### Add traces to plot ####
    #### ================== ####
    ## Linear Graph
    fig.add_trace(go.Scatter(name='Function',
                             x=x_test, y=f(x_test),
                             mode='lines',
                             line=dict(color='#000000'),
                             hovertemplate='%{y:.4f}'
                            ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=x_linear, y=n*[0],
                             mode='lines+markers',
                             line=dict(color='#000000'),
                             marker_symbol='x-thin-open',
                             marker_size=10,
                             hoverinfo='skip'
                            ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(name='Linear Grid Interpolation',
                             x=x_test, y=poly_linear(x_test),
                             mode='lines',
                             line=dict(color='#ff0000'),
                             hovertemplate='%{y:.4f}'
                            ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(name='Linear Grid Interpolation',
                             x=x_linear, y=f_linear,
                             mode='markers',
                             line=dict(color='#ff0000'),
                             marker_symbol='x-thin-open',
                             marker_size=10,
                             hovertemplate='%{x:.4f}, %{y:.4f}'
                            ),
                  row=1, col=1)

    ## Chebyshev Graph
    fig.add_trace(go.Scatter(name='Function',
                             x=x_test, y=f(x_test),
                             mode='lines',
                             line=dict(color='#000000'),
                             hovertemplate='%{y:.4f}'
                            ),
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=x_chebyshev, y=n*[0],
                             mode='lines+markers',
                             line=dict(color='#000000'),
                             marker_symbol='x-thin-open',
                             marker_size=10,
                             hoverinfo='skip'
                            ),
                  row=1, col=2)
    fig.add_trace(go.Scatter(name='Chebyshev Grid Interpolation',
                             x=x_test, y=poly_chebyshev(x_test),
                             mode='lines',
                             line=dict(color='#0000ff'),
                             hovertemplate='%{y:.4f}'
                            ),
                  row=1, col=2)
    fig.add_trace(go.Scatter(name='Chebyshev Grid Interpolation',
                             x=x_chebyshev, y=f_chebyshev,
                             mode='markers',
                             line=dict(color='#0000ff'),
                             marker_symbol='x-thin-open',
                             marker_size=10,
                             hovertemplate='%{x:.4f}, %{y:.4f}'
                            ),
                  row=1, col=2)

    ## Interpolation Difference Graph
    fig.add_trace(go.Scatter(name='Linear Grid Interpolation',
                             x=x_test, y=f(x_test)-poly_linear(x_test),
                             mode='lines',
                             line=dict(color='#ff0000'),
                             hovertemplate='%{y:.4e}'
                            ),
                  row=1, col=3)
    fig.add_trace(go.Scatter(name='Chebyshev Grid Interpolation',
                             x=x_test, y=f(x_test)-poly_chebyshev(x_test),
                             mode='lines',
                             line=dict(color='#0000ff'),
                             hovertemplate='%{y:.4e}'
                            ),
                  row=1, col=3)

    #### =========== ####
    #### Grid Layout ####
    #### =========== ####
    ## Update x-axis properties
    fig.update_xaxes(title_text=r'$x$',
                     row=1, col=2
                    )
    fig.update_xaxes(range=[L[0],L[1]],
                     gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB
                     gridwidth=1,
                     zerolinecolor='#000000',
                     zerolinewidth=2,
                     linecolor='#000000',
                     linewidth=1,
                     ticks='outside',
                     ticklen=5,
                     tickwidth=2,
                     minor_showgrid=True,
                     minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                     minor_ticks='inside',
                     minor_ticklen=5,
                     minor_tickwidth=2,
                     minor_griddash='dot',
                     hoverformat='.4f'
                    )

    ## Update y-axis properties
    fig.update_yaxes(title_text=r'$f(x)$',
                     row=1, col=1
                    )
    fig.update_yaxes(title_text=r'$f(x)$',
                     row=1, col=2
                    )
    fig.update_yaxes(title_text=r'$f(x) - p(x)$',
                     row=1, col=3
                    )
    fig.update_yaxes(title_standoff=0,
                     gridcolor='rgba(153, 153, 153, 0.75)', #999999 in RGB, 0.75 opacity
                     gridwidth=1,
                     zerolinecolor='#000000',
                     zerolinewidth=2,
                     linecolor='#000000',
                     linewidth=1,
                     ticks='outside',
                     ticklen=5,
                     tickwidth=2,
                     minor_showgrid=True,
                     minor_gridcolor='rgba(221, 221, 221, 0.50)', #DDDDDD in RGB, 0.50 opacity
                     minor_ticks='inside',
                     minor_ticklen=5,
                     minor_tickwidth=2,
                     minor_griddash='dot',
                    )

    ## Update figure layout
    fig.update_layout(height=600, width=1500,
                      plot_bgcolor='#ffffff',
                      hovermode='x unified',
                      showlegend=False,
                     )

    return fig
