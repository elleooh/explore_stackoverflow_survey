import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest

def create_contigency_table(df, col_ind, col_res, res_val_lst):
	'''
	INPUT:
	df - the pandas dataframe you want to search
	col_ind - the column name of the independent variable
	col_res - the column name of the response variable

	OUTPUT:
	contingency_df - contingency table for chi-2 test
	'''

	df1 = pd.DataFrame(df.groupby(col_ind)[col_res].sum())
	df1.rename(columns={col_res: res_val_lst[0]}, inplace=True)

	df2 = pd.DataFrame(df.groupby(col_ind).size()-df.groupby(col_ind)[col_res].sum())
	df2.rename(columns={0: res_val_lst[1]}, inplace=True)

	contingency_df = pd.merge(df1, df2, left_index=True, right_index=True)
	return contingency_df

def print_chi2_test_result(df, col_ind, col_res, res_val_lst):
	'''
	INPUT:
	df - the pandas dataframe you want to search
	col_ind - the column name of the independent variable
	col_res - the column name of the response variable
	res_val_lst - list of values for the response variable

	OUTPUT:
	No output - print out the p-value for chi2 independence test
	'''

	contingency_df = create_contigency_table(df, col_ind, col_res, res_val_lst)
	p_value = chi2_contingency(contingency_df.astype(int))[1]
	print('The p_value for chi-square test for independence between {0} and {1} is {2:.2f}'.format(col_ind, col_res, p_value))

def check_significance(df, col_ind, col_res, val, p_0=0.5, sig_level=0.05):
	'''
	INPUT:
	df - the pandas dataframe you want to search
	col_ind - the column name of the independent variable
	col_res - the column name of the response variable
	val - column value of the col_ind
	p_0 - probability under Null hypothesis (default to be 0.5)
	sig_level - significance level (default to be 0.5)

	OUTPUT:
	'yes' or 'no' depends on whether p-value is lower than the significance level
	'''

	count = sum((df[col_ind] == val) & (df[col_res] == 1))
	nobs = sum(df[col_ind] == val)
	p_a = count/nobs

	# one-sided test 
	alternative = 'smaller' if p_a < p_0 else 'larger'

	# test for proportions based on normal z test
	stat, pval = proportions_ztest(count, nobs, p_0, alternative)
	return 'yes' if pval < sig_level else 'no'

