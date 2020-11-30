def binarize_col(df, col, value_one_lst):
	'''
	INPUT
	df - the pandas dataframe you want to manipulate
	col - the column in the df where you want to turn the value to be either 1 or 0
	value_one_lst - if the column value is in this list of values, we turn it into 1; if not, turn it into 0

	OUTPUT
	df - a dataframe with an additional column that indicates binary form of the original col   
	'''

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

	df = df.dropna(subset =[col], axis=0)
	if remv_lst:
		df = df.drop(df[df[col].isin(remv_lst)].index)
	# drop those categories where the total entries < 30 because the sample size is too small for hypothesis test's normal distribution assumption 
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
	# to make the comparison for meaningful, if the dev type is 'Web developer' get the second dev type 
	if col_series.split(';')[0].strip() == 'Web developer' and col_series.split(';')[1].strip():
		# retrieve more granular developer type if the developer type is 'Developer with a statistics or mathematics background'. 
		# for example, most of them indicated they are 'Data scientist' so it makes more sense to combine them with 'Data scientist'
		if len(col_series.split(';')) > 2 and str(col_series.split(';')[1]).strip() == 'Developer with a statistics or mathematics background':
			return str(col_series.split(';')[2]).strip()
		else:
			return str(col_series.split(';')[1]).strip()
	else:
		return str(col_series.split(';')[0]).strip()


def clean_dev_type(df, col, devTypes_lst):
	'''
	INPUT
	df - the pandas dataframe you want to manipulate
	col - the feature column (i.e. 'DeveloperTypeCombined')
	devTypes_lst - list of all developer type column names

	OUTPUT
	df - a dataframe with cleaned dev type column    
	'''

	# combine all different types of developer types entries into one column
	df.loc[:, col] = df[devTypes_lst].apply(lambda x: ';'.join(x.dropna().astype(str)).strip(),axis=1)

	df.dropna(subset =[col], axis=0)

	# drop where 'DeveloperTypeCombined' is empty (not null)
	df = df.drop(df[df[col]==''].index)

	# get more granular dev type than 'web developer'
	df[col] = df[col].apply(get_granular_dev_type)

	# assign 'QA engineers' to 'Other' type since there are only two of them
	df.loc[df[col] == 'Quality assurance engineer', col] = 'Other'

	# assign 'Developer with a statistics or mathematics background' as 'Data scientist', since most of them indicated themselves also as 'Data scientist'
	df.loc[df[col] == 'Developer with a statistics or mathematics background', col] = 'Data scientist'
	return df
