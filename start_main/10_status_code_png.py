import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from sqlalchemy import create_engine

mysql_host = input("数据库地址(回车为localhost本地数据库)：") or "localhost"
mysql_user = input("数据库用户：")
mysql_pwd = input("数据库密码：")
mysql_db = input("数据库名或者回车使用默认(Log_format_DB.py自动创建的库)：") or "log_info_db"

connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pwd,
    database=mysql_db
)

# SQLAlchemy连接
engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}")

log_info_table = input("输入表名或者回车使用默认(为Log_format_DB.py自动创建的表)：") or "log_data_table"
query = f"SELECT * FROM {log_info_table}"
data = pd.read_sql(query, con=engine)

status_counts = data['status_code'].value_counts()

total_count = status_counts.sum()
percentage_threshold = 0.01  # 百分比阈值
other_percentage = 0.0
other_count = 0
filtered_counts = status_counts[status_counts / total_count >= percentage_threshold]

if len(filtered_counts) < len(status_counts):
    other_count = status_counts[status_counts / total_count < percentage_threshold].sum()
    other_percentage = other_count / total_count
    filtered_counts['其他'] = other_count

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(8, 6))
plt.pie(filtered_counts, labels=filtered_counts.index,
        autopct=lambda p: f'{p:.2f}% ({int(round(p * total_count / 100))})')
plt.title('响应状态统计')

plt.savefig(f'{log_info_table}的响应状态统计.png')
plt.show()