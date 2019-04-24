import pandas as pd
import sys
import os
import numpy as np

'''The Object Structurer: A script to make DAMS-structured objects from staging folders

Step 1: Have the user provide the root directory we want to look at

An example path to try: /mnt/digital-staging/Mexican-Broadsides/batch2/Working_Files'''

user_path = input("Enter the absolute path of the directory containing all objects: ")
os.chdir(user_path)
folders = [name for name in os.listdir(".") if os.path.isdir(name)]

# Make a list of the files within the folders
files = []
for f in folders:
    file = sorted(os.listdir(f))
    files.append(file)
    continue

# Remove any Thumbs.db files in our list
for file in files:
    while 'Thumbs.db' in file: file.remove('Thumbs.db')    
    
# Give the user some textual output of the files, then report total number of objects
print("Here is a sample of the files:")
print('\n',files[0:15])
print('\n')
print("There are",len(files),"total objects")

# Make a dictionary where the key is the bib/folder, and the value is one or more files
listing_dict = dict(zip(folders, files))

# Make our initial dataframe using the dictionary
df = pd.DataFrame.from_dict(listing_dict, orient='index', columns=['file_1', 'file_2'])

# Stack the datafame, reset index
df2 = df.stack()
df2 = df2.reset_index()
df2.index.name = None

# Find duplicates
arks = df2["level_0"]
dupe_df = df2[arks.isin(arks[arks.duplicated()])]
dupe_arks = dupe_df["level_0"]
dupe_arks = dupe_arks.unique()

# Make the duplicates dataframe
dupe_df = pd.DataFrame({'level_0':dupe_arks})

# Concatenate the two dataframes
final_df = pd.concat([df2, dupe_df], sort=True, ignore_index=True)

# Sort so that object header rows are grouped with components
final_df = final_df.sort_values(by=['level_0','level_1'], na_position='first')

# Give the user a sample of the dataFrame
print(final_df[0:50])

# Print out a csv of the final dataFrame
final_df.to_csv('~/Documents/md_structured.csv')
print("Congratulations! I've output a file in your Documents folder called 'md_structured.csv'")