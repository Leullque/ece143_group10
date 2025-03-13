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
1. run python3 clean_*.py  
   Generating new .csv files in /archive
2. import *read from *_read.py  
   Returning cleaned pandas.DataFrame

### How to Run
Note: make sure all modules are installed and all cleaned datasets are stored in /archive as .zip files
1. To perform EOQ analysis:  
python3 EOQ.py  
2. To train and evaluate ML models:  
python3 prediction.py  
3. To visualize the data and train the model:  
run visualization.ipynb  

### Third-party modules
- pandas
- matplotlib
- numpy
- seaborn
- regex
- spicy
- sklearn
- zipfile
