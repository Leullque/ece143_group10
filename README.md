# ece143_group10
### Final project
- This is the final project of inventory analysis for group 10
- We present the datasets, data cleaning methods, visualization, prediction work here.

### File structure
1. /archive: zipped datasets
2. /modules/cleaning: methods used in cleaning
3. /modules/visualization: methods used in visualization
4. EOQ.py: perform EOQ analysis
5. prediction.py: perform model training and evaluation
6. visualization.ipynb: visualization part and exploratory data analysis

### How to clean data:
run python3 clean_.py -> new .csv files generated in /archive -> generate zip files from this
import _read.py -> call _read function to return assimilated dataframes -> generate zip files from this
Cleaned data is stored back in ./archive folder

### How to Run
Note: make sure all modules are installed  
To perform EOQ analysis:  
- python3 EOQ.py  
To train and evaluate ML models:  
- python3 prediction.py  
To visualize and train the model:  
- run visualization.ipynb  

### Third-party modules
- pandas
- matplotlib
- numpy
- seaborn
- regex
- spicy
- sklearn
- zipfile
