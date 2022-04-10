import dataset
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
import numpy as np
import pandas as pd
import seaborn as sns
# read the customer user input database
cus_UI_db='sqlite:///DevDb.db'
tablename = 'app_info'
db = pd.read_sql(tablename,cus_UI_db)
print(db['gender'])
sns.set_theme(style="white")

# Plot miles per gallon against horsepower with other semantics
sns.relplot(x="id", y="gender", hue="age", size="fnews",
            sizes=(40, 400), alpha=.5, palette="muted",
            height=6, data=db)
