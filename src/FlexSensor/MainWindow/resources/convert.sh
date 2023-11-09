#!/bin/bash

# Convert .ui files to .py files
for ui in *.ui; do
    pyside6-uic $ui > ../view/${ui%.*}.py
done
 pyside6-rcc ../../resources.qrc -o ../../resources_rc.py
