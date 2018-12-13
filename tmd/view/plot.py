"""Plotting functions of tmd"""

import numpy as _np
from tmd import Topology as _tm
from tmd.view import view as _view
from tmd.view import common as _cm
from tmd.Topology import analysis


def barcode(ph, new_fig=True, subplot=False, color='b', linewidth=1.2, **kwargs):
    """
    Generates a 2d figure (barcode) of the persistent homology
    of a tree as it has been computed by
    Topology.get_persistent_homology method.
    """
    # Initialization of matplotlib figure and axes.
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    ph_sort = analysis.sort_ph(ph)

    for ip, p in enumerate(ph_sort):
        ax.plot(p[:2], [ip, ip], c=color, linewidth=linewidth)

    kwargs['title'] = kwargs.get('title', 'Persistence barcode')
    kwargs['xlabel'] = kwargs.get('xlabel', 'Lifetime: radial distance from soma')

    _cm.plt.ylim([-1, len(ph_sort)])
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def barcode_enhanced(ph, new_fig=True, subplot=False, linewidth=1.2, valID=2, cmap=_cm.plt.cm.jet, **kwargs):
    """
    Generates a 2d figure (barcode) of the persistent homology
    of a tree enhanced by a parameter encodes in ph[valID]
    """
    # Initialization of matplotlib figure and axes.
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    val_max = _np.max(ph, axis=0)[valID]

    # Hack for colorbar creation
    Z = [[0,0],[0,0]]
    levels = _np.linspace(0.0,val_max,200)
    CS3 = _cm.plt.contourf(Z, levels, cmap=cmap)

    def sort_ph_enhanced(ph, valID):
        """
        Sorts barcode according to length.
        """
        ph_sort = [p[:valID+1] + [_np.abs(p[0] - p[1])] for p in ph]
        ph_sort.sort(key=lambda x: x[valID+1])
        return ph_sort

    ph_sort = sort_ph_enhanced(ph, valID)

    for ip, p in enumerate(ph_sort):
        ax.plot(p[:2], [ip, ip], c=cmap(p[valID]/val_max), linewidth=linewidth)

    kwargs['title'] = kwargs.get('title', 'Barcode of p.h.')
    kwargs['xlabel'] = kwargs.get('xlabel', 'Lifetime')
    _cm.plt.ylim([-1, len(ph_sort)])
    _cm.plt.colorbar(CS3)

    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def diagram(ph, new_fig=True, subplot=False, color='b', alpha=1.0, edgecolors='black', s=30, **kwargs):
    """
    Generates a 2d figure (ph diagram) of the persistent homology of a tree.
    """
    # Initialization of matplotlib figure and axes.
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)

    bounds_max = _np.max(_np.max(ph))
    bounds_min = _np.min(_np.min(ph))
    _cm.plt.plot([bounds_min, bounds_max], [bounds_min, bounds_max], c='black')

    ax.scatter(_np.array(ph)[:,0], _np.array(ph)[:,1], c=color, alpha=alpha, edgecolors=edgecolors, s=s)

    kwargs['title'] = kwargs.get('title', 'Persistence diagram')
    kwargs['xlabel'] = kwargs.get('xlabel', 'End radial distance from soma')
    kwargs['ylabel'] = kwargs.get('ylabel', 'Start radial distance from soma')

    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def persistence_image(ph, new_fig=True, subplot=111, xlims=None, ylims=None, masked=False, colorbar=False,
             norm_factor=None, threshold=0.01, vmin=None, vmax=None, cmap=_cm.plt.cm.jet, **kwargs):
    '''Plots the gaussian kernel
       of the ph diagram that is given.
    '''
    if xlims is None or xlims is None:
        xlims, ylims = analysis.get_limits(ph, coll=False)

    Zn = analysis.get_persistence_image_data(ph, norm_factor=norm_factor, xlims=xlims, ylims=ylims)
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)

    if masked:
        Zn = _np.ma.masked_where((threshold > Zn), Zn)

    cax = ax.imshow(_np.rot90(Zn), vmin=vmin, vmax=vmax, cmap=cmap, interpolation='bilinear', extent=xlims+ylims)

    if colorbar:
        _cm.plt.colorbar(cax)

    kwargs['xlim'] = xlims
    kwargs['ylim'] = ylims
    kwargs['title'] = kwargs.get('title', 'Persistence image')
    kwargs['xlabel'] = kwargs.get('xlabel', 'End radial distance from soma')
    kwargs['ylabel'] = kwargs.get('ylabel', 'Start radial distance from soma')

    return Zn, _cm.plot_style(fig=fig, ax=ax, **kwargs)


def persistence_image_diff(Z1, Z2, new_fig=True, subplot=111, xlims=None, ylims=None,
                           norm=True, vmin=-1., vmax=1., cmap=_cm.plt.cm.jet, **kwargs):
    """Takes as input two images as exported from the gaussian kernel
       plotting function, and plots their difference.
    """
    if xlims is None or xlims is None:
        xlims, ylims = ((0,100), (0,100))

    difference = analysis.get_image_diff_data(Z1, Z2, norm=norm)
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    ax.imshow(_np.rot90(difference), vmin=vmin, vmax=vmax, cmap=cmap,
              interpolation='bilinear', extent=xlims+ylims)

    kwargs['xlim'] = xlims
    kwargs['ylim'] = ylims
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def persistence_image_add(Z2, Z1, new_fig=True, subplot=111, xlims=None, ylims=None,
                          norm=True, vmin=0, vmax=2., cmap=_cm.plt.cm.jet, **kwargs):
    """Takes as input two images as exported from the gaussian kernel
       plotting function, and plots their addition.
    """
    if xlims is None or xlims is None:
        xlims, ylims = ((0,100), (0,100))

    addition = analysis.get_image_add_data(Z1, Z2, norm=norm)
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    ax.imshow(_np.rot90(addition), vmin=vmin, vmax=vmax, cmap=cmap,
              interpolation='bilinear', extent=xlims+ylims)

    kwargs['xlim'] = xlims
    kwargs['ylim'] = ylims
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def persistence_image_average(ph_list, new_fig=True, subplot=111, xlims=None, ylims=None, bins=100j,
                  norm_factor=1.0, masked=False, vmin=None, vmax=None, cmap=_cm.plt.cm.jet, **kwargs):
    """Merges a list of ph diagrams and plots their respective average image.
    """
    av_imgs = analysis.get_average_persistence_image(ph_list, xlims=xlims, ylims=ylims,
                                                     bins=bins, **kwargs)
    if xlims is None or xlims is None:
        xlims, ylims = analysis.get_limits(ph_list)

    if vmin is None:
        vmin = _np.min(av_imgs)
    if vmax is None:
        vmax = _np.max(av_imgs)

    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    ax.imshow(_np.rot90(av_imgs), vmin=vmin, vmax=vmax, cmap=cmap,
              interpolation='bilinear', extent=xlims+ylims)

    kwargs['xlim'] = xlims
    kwargs['ylim'] = ylims
    kwargs['title'] = kwargs.get('title', 'Average persistence image')
    kwargs['xlabel'] = kwargs.get('xlabel', 'End radial distance from soma')
    kwargs['ylabel'] = kwargs.get('ylabel', 'Start radial distance from soma')

    return av_imgs, _cm.plot_style(fig=fig, ax=ax, **kwargs)


def start_length_diagram(ph, new_fig=True, subplot=False, color='b', alpha=1.0, **kwargs):
    '''Plots the transformed ph diagram that represents lengths and starting points
       of a component.
    '''
    from tmd.Topology.statistics import transform_ph_to_length
    ph_transformed = transform_ph_to_length(ph)
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)

    for p in ph:
        ax.scatter(p[0], p[1], c=color, edgecolors='black', alpha=alpha)

    kwargs['title'] = kwargs.get('title', 'Transformed Persistence diagram')
    kwargs['xlabel'] = kwargs.get('xlabel', 'Start of the component')
    kwargs['ylabel'] = kwargs.get('ylabel', 'Length of the component')
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def histogram_stepped(ph, new_fig=True, subplot=False, color='b', alpha=0.7, **kwargs):
    '''Extracts and plots the stepped histogram of a persistent
       homology array.
    '''
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    hist_data = analysis.histogram_stepped(ph)
    ax.fill_between(hist_data[0][:-1], 0, hist_data[1], color=color, alpha=alpha)
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def histogram_stepped_population(ph_list, new_fig=True, subplot=False, color='b', alpha=0.7, **kwargs):
    '''Extracts and plots the stepped histogram of a list of persistence diagrams.
       The histogram is normalized acording to the number of persistence diagrams.
    '''
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    hist_data = analysis.histogram_stepped(analysis.collapse(ph_list))
    ax.fill_between(hist_data[0][:-1], 0, hist_data[1]/len(ph_list), color=color, alpha=alpha)
    return _cm.plot_style(fig=fig, ax=ax, **kwargs)


def histogram_horizontal(ph, new_fig=True, subplot=False, bins=100, color='b', alpha=0.7, **kwargs):
    '''Extracts and plots the binned histogram of a persistent
       homology array.
    '''
    fig, ax = _cm.get_figure(new_fig=new_fig, subplot=subplot)
    hist_data = analysis.histogram_horizontal(ph, num_bins=bins)
    ax.fill_between(hist_data[0][:-1], 0, hist_data[1], color=color, alpha=alpha)

    return _cm.plot_style(fig=fig, ax=ax, **kwargs)
