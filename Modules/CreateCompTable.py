import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import Modules.InferentialStatistics as s

def total_count(df, col1, col2, look_for):
    '''
    INPUT:
    df - the pandas dataframe you want to search
    col1 - the column name you want to look through
    col2 - the column you want to count values from
    look_for - a list of strings you want to search for in each row of df[col]

    OUTPUT:
    new_df - a dataframe of each look_for with the count of how often it shows up
    '''

    new_df = defaultdict(int)

    for val in look_for:
        #loop through rows
        for idx in range(df.shape[0]):
            #if the ed type is in the row add 1
            if val == df[col1][idx]:
                new_df[val] += int(df[col2][idx])
    new_df = pd.DataFrame(pd.Series(new_df)).reset_index()
    new_df.columns = [col1, col2]
    new_df.sort_values('count', ascending=False, inplace=True)
    return new_df

def create_value_count_table(df, col, possible_vals_lst):
    '''
    INPUT 
    df - a dataframe holding the column of interest
    col - col name of your interest
    possible_vals_lst - a list of possible value for the col
    
    OUTPUT
    new_df - a dataframe with the count of respondents associated with each value in col
    '''

    new_df = df[col].value_counts().reset_index()
    new_df.rename(columns={'index': 'value', col: 'count'}, inplace=True)
    new_df = total_count(new_df, 'value', 'count', possible_vals_lst)
    new_df.set_index('value', inplace=True)
    return new_df

def create_comp_table(df1, df2, col1, col2, col3, dic):
    '''
    INPUT 
    df1 - a dataframe where the response variable value == 1
    df2 - a dataframe where the response variable value == 0
    col1 - designated col name for response variable value == 1 (e.g. 'agree %')
    col2 - designated col name for response variable value == 0 (e.g. 'disagree %')
    col3 - designated col name (e.g.'difference %')
    dic - dictionary that holds the ranking for each feature column value based on a specified order
        
    OUTPUT
    comp_df - a dataframe with comparison of response variable value with regard to each feature variable category
    '''

    # calculate percentage
    comp_df = pd.merge(df1, df2, left_index=True, right_index=True)
    comp_df['total count'] = comp_df['count_x']+comp_df['count_y']
    comp_df[col1] = comp_df['count_x']/comp_df['total count']
    comp_df[col2] = comp_df['count_y']/comp_df['total count']
    comp_df[col3] = comp_df[col1] - comp_df[col2]

    comp_df = comp_df.reset_index()
    comp_df = comp_df[['value', 'total count',col1, col2, col3]]

    # if dic exists, rank value by the rank presented in dic
    if dic:
        comp_df.loc[:, 'rank'] = comp_df['value'].apply(lambda col: dic[col])
        comp_df = comp_df.sort_values(by=['rank'])[['value', 'total count', col1, col2, col3]]

    comp_df = comp_df.round(2)
    return comp_df


def plot_comp_table(df, col_ind, col_res, rank_order_lst=None):
    '''
    INPUT 
    df - a dataframe holding the column of interest
    col_ind - the column name of the independent variable
    col_res - the column name of the response variable
    rank_order_lst - designated col name for response variable value == 0 (e.g. 'disagree %')
        
    OUTPUT
    No output - display comp_df based on the degree of the difference %
    '''

    # create two dataframes (i.e. agree and disagree) based on survey response
    agree_df = df.loc[df[col_res] == 1, :]
    disagree_df = df.loc[df[col_res] == 0, :]

    # plot the % of respondents agree and disagree with the survey question
    possible_vals_lst = list(df[col_ind].unique())
    agree_perc = create_value_count_table(agree_df, col_ind, possible_vals_lst)
    disagree_perc = create_value_count_table(disagree_df, col_ind, possible_vals_lst)

    col_ind_dic = None
    if rank_order_lst:
        # create a dictionary with ranking to be able to plot by rank later 
        col_ind_dic = dict(zip(rank_order_lst, range(len(rank_order_lst))))

    comp_df = create_comp_table(agree_perc, disagree_perc, 'agree %', 'disagree %', 'difference %', col_ind_dic)

    # check if the diff is statistically significant
    for val in possible_vals_lst:
        comp_df.loc[comp_df['value'] == val, 'significant?'] = s.check_significance(df, col_ind, col_res, val)

    return comp_df.style.bar(subset=['difference %'], align='mid', color=['#d65f5f', '#5fba7d'])






