"""
data_subset.py:
Takes a giant CSV and subsets it based on license, 
then outputs to individual CSVs
""" 

import os 
import pandas as pd

# Import our giant CSV into a giant DataFrame
df_cil = pd.read_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/Copy of cil_excel_object_input.csv', low_memory=False)

# Rename some columns to make it easier to work with
df_cil.rename({'Copyright status': 'copyright_status', 'CC license': 'cc_license'}, axis=1, inplace=True)

# Fill forward the copyright status to component level for Public Domain
df_cil.copyright_status = df_cil.groupby('Object Unique ID').copyright_status.apply(lambda x: x.ffill())

# Fill forward the copyright status to component level for Creative Commons
df_cil.cc_license = df_cil.groupby('Object Unique ID').cc_license.apply(lambda x: x.ffill())


"""
Make the main two DataFrames, Public Domain versus Creative Commons licenses
"""

# filter rows that are public domain
cil_pd = df_cil[df_cil['copyright_status']=='Public Domain']
cil_pd.set_index(['Object Unique ID'], inplace=True)

# Filter out null on [cc_license] to get a DataFrame with total Ceative Commons licenses 
df_cc = df_cil[df_cil.cc_license.notnull()]


"""
Further filter Creative Commons by license type and make them DataFrames
"""

# CC-BY 
cc_by = df_cc[df_cc['cc_license']=='Attribution']
cc_by.set_index(['Object Unique ID'], inplace=True)

# CC-NC 
cc_nc = df_cc[df_cc['cc_license']=='Attribution-NonCommercial']
cc_nc.set_index(['Object Unique ID'], inplace=True)

# CC-ND
cc_nd = df_cc[df_cc['cc_license']=='Attribution-NoDerivs']
cc_nd.set_index(['Object Unique ID'], inplace=True)

# CC-NC-ND
cc_nc_nd = df_cc[df_cc['cc_license']=='Attribution-NonCommercial-NoDerivs']
cc_nc_nd.set_index(['Object Unique ID'], inplace=True)

# CC-NC-SA
cc_nc_sa = df_cc[df_cc['cc_license']=='Attribution-NonCommercial-ShareAlike']
cc_nc_sa.set_index(['Object Unique ID'], inplace=True)

# CC-SA
cc_sa = df_cc[df_cc['cc_license']=='Attribution-ShareAlike']
cc_sa.set_index(['Object Unique ID'], inplace=True)



"""
Make a function to feed the DataFrames to make our samples
"""
def subsetDf(data_input):
    """
    Take a DataFrame and if it's under 500 unique objects, simply return it. 
    If the DataFrame is over 500 unique objects, it will return the first 
    500 unique objects. 
    """
    unique_obj = data_input.index.unique()
    unique_obj_list = list(unique_obj)
    if len(unique_obj) <= 500:
        return data_input
    else:
        first500 = unique_obj_list[0:500]
        data_input = data_input[data_input.index.isin(first500)]
        return data_input


"""
Set up directories, then run our function on each DataFrame then write out to the right OLR directory
"""

# Set the parent dir for everything
parent_dir = '/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/'

# Make our folders
folders = ['Public Domain','Attribution','Attribution-NonCommercial','Attribution-NoDerivs','Attribution-NonCommercial-NoDerivs','Attribution-NonCommercial-ShareAlike','Attribution-ShareAlike']
for folder in folders:
    os.mkdir(os.path.join(parent_dir,folder))

# Call our subset function on each DataFrame and output to appropriate folder
cil_pd = subsetDf(cil_pd)
cil_pd.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Public Domain/OLR_1.csv')

cc_by = subsetDf(cc_by)
cc_by.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution/OLR_1.csv')

cc_nc = subsetDf(cc_nc)
cc_nc.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution-NonCommercial/OLR_1.csv')

cc_nd = subsetDf(cc_nd)
cc_nc.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution-NoDerivs/OLR_1.csv')

cc_nc_nd = subsetDf(cc_nc_nd)
cc_nc.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution-NonCommercial-NoDerivs/OLR_1.csv')

cc_nc_sa = subsetDf(cc_nc_sa)
cc_nc.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution-NonCommercial-ShareAlike/OLR_1.csv')

cc_sa = subsetDf(cc_sa)
cc_nc.to_csv('/mnt/rdcp-staging/rdcp-0126-cil-staging-qa/Spreadsheet_Subsetting/cil_harvest_2019-09-13/OLR/Attribution-ShareAlike/OLR_1.csv')