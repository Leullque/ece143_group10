# ece143_group10
### Final project
- This is the final project of inventory analysis for group 10
- We present the datasets, data cleaning methods, visualization, prediction work here.

### File structure
1. /archive: zipped datasets
2. clean_.py: data cleanning methods 
3. _read.py: data assimilation methods
4. EOQ.py: perform EOQ analysis
5. visualization.ipynb: visualization part and exploratory data analysis

### How to Run
To clean data:

run python3 clean_.py -> new .csv files generated in /archive -> load new .csv files into dataframes
import _read.py -> call _read function to return assimilated dataframes

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
