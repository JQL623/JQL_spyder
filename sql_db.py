#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:29:35 2020

@author: JQL_2020_4_15
"""
### sqlite : relational database management system contained in a C library.

import pandas as pd
import sqlite3

conn = sqlite3.connect("/Users/jq/Documents/GitHub/JQ_datas/shared_with_LJQ/NQ_5secBar_ib.db")
cur = conn.cursor()

cur.execute("select * from NQ_2020_09_10_ib") # select * from table name

results = cur.fetchall()
print(results)

cur.close()
conn.close()


conn = sqlite3.connect("/Users/jq/Documents/GitHub/JQ_datas/shared_with_LJQ/NQ_5secBar_ib.db")
df = pd.read_sql_query("select * from NQ_2020_09_10_ib limit 5;", conn)
df

from datetime import datetime
df = pd.DataFrame(
[[1, datetime(2016, 9, 29, 0, 0) ,
datetime(2016, 9, 29, 12, 0), 'T1', 1]],
columns=["id", "departure", "arrival", "number", "route_id"])

conn = sqlite3.connect("mydb.db")
df.to_sql("daily_flights", conn, if_exists="replace")


import joblib

joblib.dump(df,'aaaaaaaaa')



