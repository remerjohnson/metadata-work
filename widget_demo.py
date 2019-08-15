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

This will automagically perform common metadata
operations on files, making a GUI via Gooey
"""

from message import display_message
import pandas as pd
import os
from argparse import ArgumentParser
from gooey import Gooey, GooeyParser


@Gooey(dump_build_config=True, program_name='Gooey Data')
def main():
    desc = 'A Gooey app that runs standard metadata processes'

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
    Take the input data file and return a pandas DataFrame
    """
    input_df = pd.read_excel(file_input)
    return input_df


def remove_double_spaces(data_input):
    """
    Take the DataFrame and remove consecutive spaces
    """
    data_input.replace(to_replace='\s\s', value=' ', regex=True, inplace=True)
    return data_input

def semicolons_to_pipes(data_input):
    """
    Take the DataFrame and within topics, replace commas with pipes
    """
    data_input.replace({'Subject:topic': r'[,;]\s'}, {'Subject:topic': ' | '}, regex=True, inplace=True)
    return data_input
    

def save_results(summarized_data, output):
    """
    Take all the data and save as Excel file
    """
    summarized_data = data_frame
    output_file = os.path.join(output, "gooey_output.xlsx")
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    summarized_data.to_excel(writer)
    writer.save()
    # Comment out to switch to csv output
    #output_file = os.path.join(output, "gooey_output.csv")
    #summarized_data.to_csv(output_file)


if __name__ == '__main__':
    conf = main()
    input_file = conf.file_input
    print('Thanks for choosing this file: ' + str(input_file))
    df = make_data_frame(conf.file_input)
    print("here's a preview\n", df.head())
    # Remove double spaces
    data_frame = remove_double_spaces(df)
    # Replace semicolons with pipes
    data_frame = semicolons_to_pipes(df)
    # Save the file as Excel
    print("Saving results data")
    save_results(data_frame, conf.output_directory)
    print("Done!")
