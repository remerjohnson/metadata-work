# Pyobstruct

This repository has a lot of utilities in their incubation stage. When they are mature, they can move to dedicated repositories.  

## `pyobstruct` 

`pyobstruct.py` is a program that can structure an object level record given a location on our shared server. This use case specifically applies to Roger collections, as it uses the folder structure to create complex objects.  

## `pyconstruct` 

`pyconstuct.py` is a program that is needed further down the line than `pyobstruct`. This is after subject wrangling and cleaning is finished. It will then merge those clean subjects into the existing object level record, joining on the `bib` column.  

## `widget_demo` 

`widget_demo.py` is a program that uses [Gooey](https://github.com/chriskiehl/Gooey), a GUI builder. The program is intended to apply many common transformations on a record, like collapsing consecutive spaces into one space, or switching delimiters.  
