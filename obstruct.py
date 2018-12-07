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
    file = os.listdir(f)
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

# Make a dictionary of a dataFrame (using the above dictionary
dict_of_df = {k: pd.DataFrame(v) for k,v in listing_dict.items()}

# Make THAT a dataFrame
df = pd.concat(dict_of_df)

# Give the user a sample of the dataFrame
print(df[0:50])

# Print out a csv of the dataFrame
df.to_csv('~/Documents/mb_struct.csv')