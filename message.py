import sys
import time

program_message = \
'''
Thanks for checking out out my program.

Here are the arguments you supplied:

{0}

-------------------------------------

This project was made using Gooey. If you'd like to contribute, you can find the
author's issue tracker on Github[1]. 

[1](https://github.com/chriskiehl/Gooey)



'''

def display_message():
  message = program_message.format('\n-'.join(sys.argv[1:])).split('\n')
  delay = 1.8 / len(message)

  for line in message:
    print(line)
    time.sleep(delay)

