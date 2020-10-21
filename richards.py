from math import e

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure


def logistic(x_vals, a=0, k=1, q=1, b=1, v=1):
    """
    Plots the parameterized logistic function for the given values of x.

    :param x_vals: list of x values to compute
    :param a: lower asymptote
    :param k: upper asymptote
    :param q: related to the value when x=0
    :param b: growth rate
    :param v: affects near which asymptote maximum growth occurs; must be positive
    :return:
    """
    if a >= k:
        raise ValueError(f"Parameter 'k' must be greater than 'a': [a={a}, k={k}]")
    if v <= 0:
        raise ValueError(f"Parameter 'v' must be postive: [v={v}]")

    return a + (k - a) / (1 + q * e ** (-b * x_vals)) ** (1 / v)


sliders = (
    slider_a,
    slider_k,
    slider_q,
    slider_b,
    slider_v,
) = (
    Slider(title='a, Lower Asymptote', value=0, start=-10, end=0, step=1, tooltips=False),
    Slider(title='k, Upper Asymptote', value=1, start=1, end=10, step=1, tooltips=False),
    Slider(title='q, Affects y at x=0', value=1, start=0.001, end=5, step=0.1, tooltips=False),
    Slider(title='b, Growth rate', value=1, start=0.01, end=3, step=0.1, tooltips=False),
    Slider(title='v, Affects where max growth occurs', value=1, start=0.01, end=5, step=0.1, tooltips=False),
)

xs_min = -10
xs_max = 10
xs_size = 100
xs = np.linspace(xs_min, xs_max, xs_size)
ys = logistic(
    x_vals=xs,
    a=slider_a.value,
    k=slider_k.value,
    q=slider_q.value,
    b=slider_b.value,
    v=slider_v.value
)

source = ColumnDataSource(data=dict(x=xs, y=ys))

plot = figure(
    plot_height=400,
    plot_width=600,
    title='Generalized Logistic Curve',
    tools='crosshair,pan,reset,save,wheel_zoom',
    # x_range=[xs_min, xs_max],
    # y_range=[-1, 2]
)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


def update_data_callback(attrname, old, new):
    """Update the plot source data"""
    global ys
    ys = logistic(
        x_vals=xs,
        a=slider_a.value,
        k=slider_k.value,
        q=slider_q.value,
        b=slider_b.value,
        v=slider_v.value
    )
    source.data = dict(x=xs, y=ys)


for s in sliders:
    s.on_change('value', update_data_callback)

params = column(
    slider_a,
    slider_k,
    slider_q,
    slider_b,
    slider_v
)

curdoc().add_root(row(plot, params, width=1000))
curdoc().title = 'Logistic'
