# ece143_group10
### Final project
- This is the final project of inventory analysis for group 10
- We present the datasets, data cleaning methods, visualization, prediction work here.

### File structure
1. /archive: zipped datasets
2. EOQ.py: perform EOQ analysis
3. visualization.ipynb: visualization part and exploratory data analysis
4. /modules/cleaning: methods used in cleaning
   1. clean_.py: data cleanning methods
   2. _read.py: data assimilation methods
5. /modules/visualization: methods used in visualization

### How to clean data:
run python3 clean_.py -> new .csv files generated in /archive -> generate zip files from this
import _read.py -> call _read function to return assimilated dataframes -> generate zip files from this
Cleaned data is stored back in ./archive folder

### How to Run
To visualize and train the model:
1. make sure all modules are installed
2. run visualization.ipynb

### Third-party modules
- pandas
- matplotlib
- numpy
- seaborn
- regex
- spicy
- sklearn
