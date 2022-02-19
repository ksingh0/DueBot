# import pandas as pd
# from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy
# import sqlite3
# def tasksetup():

#     newdata = website.data
#     headers = []
#     for i in range(len(newdata)):
#         headers.append(newdata[i][0])
#         del newdata[i][0]

#     df = pd.DataFrame(newdata)
#     df.to_html('templates/tasklist.html', justify='left')