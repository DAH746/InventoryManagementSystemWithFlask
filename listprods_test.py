from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import random
import string
from datetime import datetime
import boto3
from werkzeug.utils import secure_filename
import s3_bucket_operations
import bucket_names_object
import contains_all_urls_for_s3_buckets

con = sql.connect("InventoryDatabase.db")
con.row_factory = sql.Row

cur = con.cursor()
cur.execute("select * from Inventory")

rows = cur.fetchall();

for row in rows:
    print(row)