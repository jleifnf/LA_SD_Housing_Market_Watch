import matplotlib.pyplot as plt
import seaborn as sns

titles = {
    'OnMarketDays': 'Time on Market (Days)',
    'ClosePrice': 'Close Price ($ millions)',
    'ListPrice': 'List Price ($ millions)',
    'PriceDiffRatio': 'Price Cut Ratio'
    }


def boxplot(x, y, hue=None, order=None, data=None, title=None, c='k', figsize=(16, 9), context='notebook', savefig=False):
    """
    """
    with sns.plotting_context(context):
        if isinstance(y, list):
            fig, ax = plt.subplots(1, len(y), figsize=figsize, squeeze=False)
            for i, col in enumerate(y):
                sns.boxplot(x=x, y=col, hue=hue, order=order, fliersize=2.5, data=data, ax=ax[0, i])
                ax[0, i] = ax_params(ax[0, i], titles[col], c)
                ax[0, i].set_title('')
        elif isinstance(y, str):
            fig, ax = plt.subplots(figsize=(6.75, 12))
            sns.boxplot(x=x, y=y, hue=hue, order=order, fliersize=2.5, data=data, ax=ax)
            ax.set_ylabel(y, color=c)
            ax = ax_params(ax, title, c)
        if savefig:
            fig.savefig('figs/{}-boxplot.png'.format(title), transparent=True, dpi=200, bbox_inches='tight')
        plt.show()
        return fig, ax


def violinplot(x, y, hue=None, order=None, data=None, title=None, c='k', figsize=(16, 9), context='notebook',
               savefig=False):
    """
    """
    with sns.plotting_context(context):
        if isinstance(y, list):
            fig, ax = plt.subplots(1, len(y), figsize=figsize, squeeze=False)
            for i, col in enumerate(y):
                sns.violinplot(x=x, y=col, hue=hue, order=order, data=data, scale='count', ax=ax[0, i])
                ax[0, i] = ax_params(ax[0, i], titles[col], c)
                ax[0, i].set_title('')
        elif isinstance(y, str):
            fig, ax = plt.subplots(figsize=(6.75, 12))
            sns.violinplot(x=x, y=y, hue=hue, order=order, data=data, scale='count', ax=ax)
            ax.set_ylabel(y, color=c)
            ax = ax_params(ax, title, c)
        if savefig:
            fig.savefig('figs/{}-violinplot.png'.format(title), transparent=True, dpi=200, bbox_inches='tight')
        plt.show()
        return fig, ax


def barplot(x, y, data=None, hue=None, title=None, figsize=(16, 9), order=None,
            c='k', context='notebook', savefig=False):
    """
    """
    with sns.plotting_context(context):
        if isinstance(y, list):
            fig, ax = plt.subplots(1, len(y), figsize=figsize, squeeze=False)
            for i, col in enumerate(y):
                sns.barplot(x=x, y=col, hue=hue, order=order, data=data, errcolor=c, ci='sd', capsize=0.1, ax=ax[0, i])
                ax[0, i] = ax_params(ax[0, i], titles[col], c)
                ax[0, i].set_title('')
        elif isinstance(y, str):
            fig, ax = plt.subplots(figsize=(6.75, 12))
            sns.barplot(x=x, y=y, hue=hue, order=order, data=data, errcolor=c, ci='sd', capsize=0.1, ax=ax)
            ax = ax_params(ax, title, c)
        if savefig:
            fig.savefig('figs/{}-barplot.png'.format(title), transparent=True, dpi=200, bbox_inches='tight')
        plt.show()
        return fig, ax


def distplot(d1, d2, d1_label, d2_label=None, d1_popstat=None, d2_popstat=None,
             bins=None, kde=True, title='Histogram', figsize=(8, 4.5),
             c='k', context='notebook', savefig=False):
    """
    d1,d2             = datas to plot (bootstrapped means)
    d1_label, d2label = labels for datas
    d1_(d2_)popstat   = tuple of population/dataset (mean,stdev)
    bins              = number of equally sized bins for
    kde               = True: if to plot kernel-density; False: if to take the plot away
    lim               = axis limits (tuple: (xlim=(xmin xmax),ylim=(ymin ymax))
    """
    with sns.plotting_context(context):
        fig, ax = plt.subplots(figsize=figsize)
        sns.distplot(d1, bins=bins, kde=kde, label=d1_label, hist=False, kde_kws={"shade": True}, color='b', ax=ax)
        sns.distplot(d2, bins=bins, kde=kde, label=d2_label, hist=False, kde_kws={"shade": True}, color='r', ax=ax)
        if d1_popstat or d2_popstat:
            ymax = ax.get_ylim()[1]
            print(ymax)
            d1_mu = d1_popstat[0]
            d1_ci = [d1_mu + 2 * d1_popstat[1], d1_mu - 2.58 * d1_popstat[1]]
            d2_mu = d2_popstat[0]
            d2_ci = [d2_mu + 2 * d2_popstat[1], d2_mu - 2.58 * d2_popstat[1]]
            ax.vlines(d1_mu, 0, ymax, colors='b')
            ax.vlines(d1_ci, 0, ymax, linestyles='dashed', colors='b')
            ax.vlines(d2_mu, 0, ymax, colors='r')
            ax.vlines(d2_ci, 0, ymax, linestyles='dashed', colors='r')
            ax.set_ylim(0,ymax)
        ax = ax_params(ax, title, c)
        plt.legend()
        if savefig:
            fig.savefig('figs/{}-distplot.png'.format(title), transparent=True, dpi=200, bbox_inches='tight')
        plt.show()
        return fig, ax


def scatterplot(x, y, hue=None, data=None, title=None, figsize=(16, 9), order=None,
                c='k', context='notebook', savefig=False):
    """
    """
    with sns.plotting_context(context):
        fig, ax = plt.subplots(figsize=figsize)
        sns.scatterplot(x=x, y=y, hue=hue, data=data, ax=ax)
        ax = ax_params(ax, title, c)
        plt.legend()
        if savefig:
            fig.savefig('figs/{}-barplot.png'.format(title), transparent=True, dpi=200, bbox_inches='tight')
        plt.show()
        return fig, ax


def ax_params(ax, title, c='k'):
    ax.set_xlabel('', color=c)
    ax.set_ylabel(title, color=c)
    ax.tick_params(axis='both', pad=0, colors=c, labelcolor=c)
    ax.spines['left'].set_color(c)
    ax.spines['bottom'].set_color(c)

    for i, artist in enumerate(ax.artists):
        artist.set_edgecolor(c)
        for j in range(i * 6, i * 6 + 6):
            line = ax.lines[j]
            line.set_color(c)
            line.set_mfc(c)
            line.set_mec(c)
    return ax
