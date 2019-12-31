#!/usr/bin/env python
"""
Made with Gooey:

  / ____|                      | | |
 | |  __  ___   ___   ___ _   _| | |
 | | |_ |/ _ \ / _ \ / _ \ | | | | |
 | |__| | (_) | (_) |  __/ |_| |_|_|
  \_____|\___/ \___/ \___|\__, (_|_)
                           __/ |
                          |___/

This program will automagically perform common metadata
operations on files, making a GUI via Gooey
"""

from message import display_message
import pandas as pd
import os
from argparse import ArgumentParser
from gooey import Gooey, GooeyParser


@Gooey(dump_build_config=False, program_name='DOMMinator')
def main():
    desc = 'A Gooey (GUI) app that runs standard metadata processes'

    parser = GooeyParser(description=desc)
    # Add ability to choose a file
    parser.add_argument('file_input',
                        metavar='File Input',
                        action='store',
                        help='Select the file you want to process',
                        widget='FileChooser')
    # Add ability to save the file
    parser.add_argument('output_directory',
                        metavar='Output Directory',
                        action='store',
                        help='Choose where to save the output',
                        widget='DirChooser')

    args = parser.parse_args()
    display_message()
    return args


def make_data_frame(file_input):
    """
    Take the input data file (assuming Excel) and return a pandas DataFrame
    """
    input_df = pd.read_excel(file_input)
    return input_df

def trim_spaces(data_input):
    """
    Take the DataFrame and remove surrounding spaces on values
    """
    data_input.replace('(^\s+|\s+$)', '', regex=True, inplace=True)
    return data_input

def remove_double_spaces(data_input):
    """
    Take the DataFrame and remove consecutive spaces
    """
    data_input.replace(to_replace='\s\s', value=' ', regex=True, inplace=True)
    return data_input

def delimiters_to_pipes(data_input):
    """
    Take the DataFrame and within topics, replace commas with pipes
    """
    data_input.replace({'Subject:topic': r'[,;]\s'}, {'Subject:topic': ' | '}, regex=True, inplace=True)
    return data_input
    
def process_dates(data_input):
    """
    Try to handle dates, and start to populate the Begin + End Date columns
    """
    date_begin = []
    date_end = []
    columns = data_input.columns
    for column in columns:
        if column.lower().startswith("date"):
            for row in data_input[column]:
                if len(str(row)) == 4:
                    date_begin.append(str(row) + "-01-01")
                    date_end.append(str(row) + "-12-31")
                else:
                    date_begin.append("")
                    date_end.append("")
    data_input['date:begin'] = date_begin
    data_input['date:end'] = date_end                
    return data_input

def save_results(summarized_data, output):
    """
    Take all the data and save as Excel file
    """
    summarized_data = data_frame
    output_file = os.path.join(output, "gooey_output.xlsx")
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    summarized_data.to_excel(writer, index=False)
    writer.save()
    # Comment out to switch to csv output
    #output_file = os.path.join(output, "gooey_output.csv")
    #summarized_data.to_csv(output_file)


if __name__ == '__main__':
    conf = main()
    input_file = conf.file_input
    print('You chose this file: ' + str(input_file))
    df = make_data_frame(conf.file_input)
    print("Here's a preview:\n", df.head())
    # Strip spaces
    data_frame = trim_spaces(df)
    # Remove double spaces
    data_frame = remove_double_spaces(df)
    # Replace semicolons with pipes
    data_frame = delimiters_to_pipes(df)
    # Begin to populate Begin and End Date
    data_frame = process_dates(df)
    # Save the file as Excel
    print("Saving results data")
    save_results(data_frame, conf.output_directory)
    print("Done!")
