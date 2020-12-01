import matplotlib.pyplot as plt

def draw_hist_cat(df, col, color='#86bf91', save=True):
    '''
    INPUT:
    df - the pandas dataframe that includes the column you want to plot distribition for
    col - the column you want to plot distribition for (should include categorical values)
    save - bool value to indicate whether the plot needs to be saved (default to be True)

    OUTPUT:
    histogram of the categorical values of col in df
    '''

    feature = df[col][~df[col].isna()].sort_values()

    plt.figure(figsize=(10,6))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    n_bin = len(feature.unique())+1
    feature.hist(bins=range(n_bin), grid=False, color = color, zorder=2, rwidth=0.9, align='left')
    title_name = 'Distribution of ' + col
    plt.title(title_name, fontsize=10)
    if save:
        file_name = 'distribution_all'+ col + '.png'
        plt.savefig(file_name, dpi=300)
    plt.show()
