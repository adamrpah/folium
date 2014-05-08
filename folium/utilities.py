# -*- coding: utf-8 -*-
'''
Utilities
-------

Utility module for Folium helper functions.

'''

from __future__ import print_function
from __future__ import division
import math
from jinja2 import Environment, PackageLoader, Template

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None


def get_templates():
    '''Get Jinja templates'''
    return Environment(loader=PackageLoader('folium', 'templates'))

def legend_scaler(legend_values, max_labels=10):
    '''
    Downsamples the number of legend values so that there isn't a collision
    of text on the legend colorbar (within reason). The colorbar seems to 
    support ~10 entries as a maximum
    '''

    if len(legend_values)<max_labels:
        legend_ticks = legend_values
    else:
        legend_ticks = []
        divisor = len(legend_values)/max_labels
        for i in range(len(legend_values)):
            #We don't want the first index since the scale will have a 
            #0th value from the range. Otherwise, if the modulo is 0
            #Then we accept the value as a legend tick label
            if i!=0 and i%divisor==0:
                legend_ticks.append(legend_values[i])
            else:
                legend_ticks.append('')
    return legend_ticks


def rgb_to_hex(color_code):
    '''Converts an rgb color list to hexadecimal'''

    def _colorval_to_hexval(cval):
        '''Converts a single color to its two letter hex code'''
        div = int(cval/16)
        rem = int(cval%16)
        hexval = _numeric_to_indhex(div) + _numeric_to_indhex(rem)
        return hexval

    def _numeric_to_indhex(mathval):
        '''Converts a single color digit to its code letter in hex'''
        alphas = 'ABCDEF'
        if mathval < 10:
            return str(mathval)
        else:
            mathval = mathval-10
            return alphas[mathval]

    indhex = '#' + ''.join([_colorval_to_hexval(tcolor) for tcolor in color_code]) 
    return indhex


def hex_to_rgb(color_code):
    '''Converts a hex color to rgb'''

    def _hexval_to_colorval(hval):
        '''Converts a two letter hex to single color number'''
        div = _indhex_to_numeric(hval[0]) * 16
        rem = _indhex_to_numeric(hval[1])
        return div + rem

    def _indhex_to_numeric(letterval):
        '''Converts a single letter to a color number'''
        alphas = 'ABCDEF'
        try:
            letterval = int(letterval)
            return letterval
        except ValueError:
            letterval = alphas.index(letterval) + 10
            return letterval
    if '#'==color_code[0]:
        color_code = color_code[1:]
    separated_hexes = [color_code[i*2:i*2+2] for i in range(3)]
    indrgb = [_hexval_to_colorval(hpair) for hpair in separated_hexes]
    return indrgb

def linear_gradient(rgbList, nColors):
    """Given a list of (r, g, b) tuples, will return a list of length
    nColors where the colors are linearly interpolated between the
    (r, g, b) tuples that are given.

    Example:
    linear_gradient([(0, 0, 0), (255, 0, 0), (255, 255, 0)], 100)

    Adapted from PyGrace
    Author:Mike Stringer
    """
    def _scale(start, finish, length, i):
        """Return the value correct value of a number that is inbetween start
        and finish, for use in a loop of length *length*"""

        fraction = float(i) / (length - 1)
        raynge = finish - start
        return start + fraction * raynge


    allColors = []
    # separate (r, g, b) pairs
    for start, end in zip(rgbList[:-1], rgbList[1:]):

        # linearly intepolate between pair of (r, g, b) and add to list
        nInterpolate = 765 
        for index in range(nInterpolate):
            r = _scale(start[0], end[0], nInterpolate, index)
            g = _scale(start[1], end[1], nInterpolate, index)
            b = _scale(start[2], end[2], nInterpolate, index)
            allColors.append( (r, g, b) )

    # pick only nColors colors from the total list
    result = []
    for counter in range(nColors):
        fraction = float(counter) / (nColors - 1)
        index = int(fraction * (len(allColors) - 1)) 
        result.append(allColors[index])
    return result


def color_brewer(color_code, n=6):
    '''Generate a colorbrewer color scheme of length 'len', type 'scheme.
    Live examples can be seen at http://colorbrewer2.org/'''
    maximum_n = 253

    schemes = {'BuGn': ['#EDF8FB', '#CCECE6', '#CCECE6', '#66C2A4', '#41AE76',
                        '#238B45', '#005824'],
               'BuPu': ['#EDF8FB', '#BFD3E6', '#9EBCDA', '#8C96C6', '#8C6BB1',
                        '#88419D', '#6E016B'],
               'GnBu': ['#F0F9E8', '#CCEBC5', '#A8DDB5', '#7BCCC4', '#4EB3D3',
                        '#2B8CBE', '#08589E'],
               'OrRd': ['#FEF0D9', '#FDD49E', '#FDBB84', '#FC8D59', '#EF6548',
                        '#D7301F', '#990000'],
               'PuBu': ['#F1EEF6', '#D0D1E6', '#A6BDDB', '#74A9CF', '#3690C0',
                        '#0570B0', '#034E7B'],
               'PuBuGn': ['#F6EFF7', '#D0D1E6', '#A6BDDB', '#67A9CF', '#3690C0',
                          '#02818A', '#016450'],
               'PuRd': ['#F1EEF6', '#D4B9DA', '#C994C7', '#DF65B0', '#E7298A',
                        '#CE1256', '#91003F'],
               'RdPu': ['#FEEBE2', '#FCC5C0', '#FA9FB5', '#F768A1', '#DD3497',
                        '#AE017E', '#7A0177'],
               'YlGn': ['#FFFFCC', '#D9F0A3', '#ADDD8E', '#78C679', '#41AB5D',
                        '#238443', '#005A32'],
               'YlGnBu': ['#FFFFCC', '#C7E9B4', '#7FCDBB', '#41B6C4', '#1D91C0',
                          '#225EA8', '#0C2C84'],
               'YlOrBr': ['#FFFFD4', '#FEE391', '#FEC44F', '#FE9929', '#EC7014',
                          '#CC4C02', '#8C2D04'],
               'YlOrRd': ['#FFFFB2', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A',
                          '#E31A1C', '#B10026']}

    #Raise an error if the n requested is greater than the maximum
    if n > maximum_n:
        raise ValueError("The maximum number of colors in a ColorBrewer sequential color series is 253")

    #Only if n is greater than six do we interpolate values
    if n > 6:
        if color_code not in schemes:
            color_scheme= None
        else:
            rgb_color_scheme = [hex_to_rgb(hex_code) for hex_code in schemes.get(color_code)]
            color_scheme = [rgb_to_hex(rgb_code) for rgb_code in linear_gradient(rgb_color_scheme, n)]
    else:
        color_scheme = schemes.get(color_code, None)
    return color_scheme



def transform_data(data):
    '''Transform Pandas DataFrame into JSON format

    Parameters
    ----------
    data: DataFrame or Series
        Pandas DataFrame or Series

    Returns
    -------
    JSON compatible dict

    Example
    -------
    >>>transform_data(df)

    '''

    if pd is None:
        raise ImportError("The Pandas package is required for this functionality")

    if np is None:
        raise ImportError("The NumPy package is required for this functionality")

    def type_check(value):
        '''Type check values for JSON serialization. Native Python JSON
        serialization will not recognize some Numpy data types properly,
        so they must be explictly converted.'''
        if pd.isnull(value):
            return None
        elif (isinstance(value, pd.tslib.Timestamp) or
              isinstance(value, pd.Period)):
            return time.mktime(value.timetuple())
        elif isinstance(value, (int, np.integer)):
            return int(value)
        elif isinstance(value, (float, np.float_)):
            return float(value)
        elif isinstance(value, str):
            return str(value)
        else:
            return value

    if isinstance(data, pd.Series):
        json_data = [{type_check(x): type_check(y) for x, y in data.iteritems()}]
    elif isinstance(data, pd.DataFrame):
        json_data = [{type_check(y): type_check(z) for x, y, z in data.itertuples()}]

    return json_data


def split_six(series=None):
    '''Given a Pandas Series, get a domain of values from zero to the 90% quantile
    rounded to the nearest order-of-magnitude integer. For example, 2100 is rounded
    to 2000, 2790 to 3000.

    Parameters
    ----------
    series: Pandas series, default None

    Returns
    -------
    list

    '''

    if pd is None:
        raise ImportError("The Pandas package is required for this functionality")
    if np is None:
        raise ImportError("The NumPy package is required for this functionality")

    def base(x):
        if x > 0:
            base = pow(10, math.floor(math.log10(x)))
            return round(x/base)*base
        else:
            return 0

    quants = [0, 50, 75, 85, 90]
    # Some weirdness in series quantiles a la 0.13
    arr = series.values
    return [base(np.percentile(arr, x)) for x in quants]
