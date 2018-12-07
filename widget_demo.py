'''
Made with generous support by Gooey:
 __          __  _
 \ \        / / | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \
    \  /\  /  __/ | (_| (_) | | | | | |  __/
  ___\/__\/ \___|_|\___\___/|_| |_| |_|\___|
 |__   __|
    | | ___
    | |/ _ \
    | | (_) |
   _|_|\___/                    _ _
  / ____|                      | | |
 | |  __  ___   ___   ___ _   _| | |
 | | |_ |/ _ \ / _ \ / _ \ | | | | |
 | |__| | (_) | (_) |  __/ |_| |_|_|
  \_____|\___/ \___/ \___|\__, (_|_)
                           __/ |
                          |___/


This will automagically perform common metadata
operations on files, making a GUI via Gooey
'''

from gooey import Gooey, GooeyParser
from message import display_message
import csv 
import pandas as pd
import numpy as np

@Gooey(dump_build_config=True, program_name="Gooey Data")
def main():
  desc = "A Gooey app that runs standard metadata processes"
  file_help_msg = "Name of the file you want to process"

  my_cool_parser = GooeyParser(description=desc)

  my_cool_parser.add_argument("FileChooser", help=file_help_msg, widget="FileChooser")
  my_cool_parser.add_argument("DirectoryChooser", help=file_help_msg, widget="DirChooser")
  my_cool_parser.add_argument("FileSaver", help=file_help_msg, widget="FileSaver")
  my_cool_parser.add_argument("MultiFileSaver", help=file_help_msg, widget="MultiFileChooser")
  my_cool_parser.add_argument("directory", help="Directory to store output")

  my_cool_parser.add_argument("-w", "--writelog", default="writelogs", help="Dump output to local file")
  my_cool_parser.add_argument("-e", "--error", action="store_true", help="Stop process on error (default: No)")
  verbosity = my_cool_parser.add_mutually_exclusive_group()
  verbosity.add_argument('-t', '--verbozze', dest='verbose', action="store_true", help="Show more details")
  verbosity.add_argument('-q', '--quiet', dest='quiet', action="store_true", help="Only output on error")

  args = my_cool_parser.parse_args()
  display_message()

def here_is_smore():
  pass


if __name__ == '__main__':
  main()
