import matplotlib.pyplot as plt

def draw_hist_cat(df, col, color='#86bf91'):
    '''
    INPUT:
    df - the pandas dataframe that includes the column you want to plot distribition for
    col - the column you want to plot distribition for (should include categorical values)

    OUTPUT:
    histogram of the categorical values of col in df
    '''

    feature = df[col][~df[col].isna()].sort_values()
    
    fig = plt.figure(figsize=(10,6))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    n = len(feature.unique())
    feature.hist(bins=range(n+1), grid=False, color = color, zorder=2, rwidth=0.9, align='left')
    title_name = 'Distribution of ' + col
    plt.title(title_name, fontsize=10)
    plt.show()