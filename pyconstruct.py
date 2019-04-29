import pandas as pd

# Read in rough OLR as first dataframe
df1 = pd.read_csv('~/Github/dams-metadata/mexican-broadsides/batch3/mexican_broadsides_b3_roger_export.csv')

# Read in cleaned up subjects
df2 = pd.read_excel('~/Github/dams-metadata/mexican-broadsides/subjects/mexican_broadsides_withfast_b3.xlsx') 

# Merge on 'bib' column in both dataframes
dff = pd.merge(left=df1,right=df2, how='left', left_on='bib', right_on='bib')

# Uncomment to make the file! 
dff.to_csv('~/Documents/mb3_OLR_with_subj.csv')