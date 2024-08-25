# preg-graph

**preg-graph** is a simple visualisation utility built with Python and PyPlot. 
It pulls pregnancy data from a CSV file, and exports a nice looking graph with all the relative information. 

![preg-graph](/preg-graph.jpg?raw=true "pre-graph")

## Requirements

Currently, the first column of the input CSV file needs to be called `Week` and must be reserved to the week number. 
Any other column can be customized to whatever sympthom.

## Usage

By simply calling `py .\pre-graph.py`, you will pull the pregnancy data stored in `data.csv` and export a `graph.png` file. 

Alternatively, you could pass additional arguments:

| Args             | Description                                  |
|------------------|----------------------------------------------|
| `-i` `--input`   | Path to the input CSV file to be read.       |
| `-o`, `--output` | Path of the output PNG graph to be exported. |
| `--columns`      | Amount of graph columns.                     |
| `--style`        | Name of the graph style.                     |
| `--dpi`          | DPI resolution of the exported graph.        |

For example `py .\pre-graph.py -i my_data.csv -o /output/my_graph.png --columns 2 --dpi 150` will pull the data from `my_data.csv` 
and export a 2-column graph to the `/output` subfolder, with the resolution of 150 DPI.

## Styling

You can add your own styling by editing the `style.py`. 
The styling options follow the requirements of [PyPlot](https://www.w3schools.com/python/matplotlib_line.asp).
