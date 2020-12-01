def binarize_col(df, col, value_one_lst):
    '''
	INPUT
	df - the pandas dataframe you want to manipulate
	col - the column in the df where you want to turn the value to be either 1 or 0
	value_one_lst - if the column value is in this list of values, we turn it into 1
	; if not, turn it into 0

	OUTPUT
	df - a dataframe with an additional column that indicates binary form of the original col
	'''

	# drop all rows with Nan values in col
	# because the row is of no value when the response varialbe is Nan
    df = df.dropna(subset=[col], axis=0)
    df.loc[df[col].isin(value_one_lst), str(col)+'_bin'] = 1
    df.loc[~df[col].isin(value_one_lst), str(col)+'_bin'] = 0
    return df


def clean_df(df, col, remv_lst=None):
    '''
    INPUT
    df - the pandas dataframe you want to manipulate
    col - the feature column that needs to be cleaned
    remv_lst - a list of row values where rows need to be removed if the value is in this list

    OUTPUT
    df - a cleaned dataframe
	'''

    # drop all rows with Nan values in col
    # because we are interested in how the feature column interacts with the response variable
    # the Nan value in feature col would have little to no meaning for our purposes
    df = df.dropna(subset =[col], axis=0)
    if remv_lst:
        df = df.drop(df[df[col].isin(remv_lst)].index)

    # drop those categories where the total entries < 30
    # because the sample size is too small for hypothesis test's normal distribution assumption
    small_cat = list(df[col].value_counts().loc[df[col].value_counts().values < 30].index)
    df = df.drop(df[df[col].isin(small_cat)].index)
    return df

def get_granular_dev_type(col_series):
    '''
    INPUT
    col_series - column series

    OUTPUT
    col_series split in a certain way
    '''

    # since 70% respondents' first dev type choice is 'Web developer',
    # if the dev type is 'Web developer' get the second dev type
    if col_series.split(';')[0].strip() == 'Web developer' and col_series.split(';')[1].strip():
        # retrieve more granular developer type
        # if the developer type is 'Developer with a statistics or mathematics background'
        if len(col_series.split(';')) > 2 and \
        str(col_series.split(';')[1]).strip() == 'Developer with a statistics or mathematics background':
            return str(col_series.split(';')[2]).strip()
        return str(col_series.split(';')[1]).strip()
    return str(col_series.split(';')[0]).strip()


def clean_dev_type(df, col, dev_types_lst):
    '''
    INPUT
    df - the pandas dataframe you want to manipulate
    col - the feature column (i.e. 'DeveloperTypeCombined')
    devTypes_lst - list of all developer type column names

    OUTPUT
    df - a dataframe with cleaned dev type column
    '''

    # combine all different types of developer types entries into one column
    df.loc[:, col] = df[dev_types_lst].apply(lambda x:
    	';'.join(x.dropna().astype(str)).strip(),axis=1)

    # drop all rows with Nan values in col
    # because we are interested in how the feature column interacts with the response variable
    # the Nan value in feature col would have little to no meaning for our purposes
    df.dropna(subset =[col], axis=0)

    # drop where 'DeveloperTypeCombined' is empty (not null)
    df = df.drop(df[df[col]==''].index)

    # get more granular dev type than 'web developer'
    df[col] = df[col].apply(get_granular_dev_type)

    # assign 'QA engineers' to 'Other' type since there are only two of them
    df.loc[df[col] == 'Quality assurance engineer', col] = 'Other'

    # most of 'Developer with a statistics or mathematics background' are 'Data scientist'
    df.loc[df[col] == 'Developer with a statistics or mathematics background', col] = 'Data scientist'
    return df
