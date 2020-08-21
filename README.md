# Metadata Work

This repository is a general holding place for a lot of the work I've done in Metadata Services. It contains a lot of coding projects in their incubation stage. When projects are very mature, they may move to dedicated repositories.  

The `/documentation` folder holds Jupyter notebooks that work through and describe processes I've done. I typically use `pandas` and other python libraries in order to work with data.  

# Coding Projects

## Object Structurer (pyobstruct)

`pyobstruct.py` is a program that can structure an object level record given a location on our shared server. This use case specifically applies to Roger collections, as it uses the folder structure to create complex objects.  

## Object Constructer (pyconstruct)

`pyconstuct.py` is a program that is needed further down the line than `pyobstruct`. This is after subject wrangling and cleaning is finished. It will then merge those clean subjects into the existing object level record, joining on the `bib` column.  
