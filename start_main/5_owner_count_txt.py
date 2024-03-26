import mysql.connector
import csv

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

cursor = connection.cursor()
log_info_table = input("输入表名或者回车使用默认(为Log_format_DB.py自动创建的表)：") or "log_data_table"
owner_rank = input("输入需要排行数/回车排出前十：") or 10

query = f"SELECT owner, COUNT(*) AS count FROM {log_info_table} WHERE owner IS NOT NULL GROUP BY owner ORDER BY count DESC LIMIT {owner_rank}"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

with open(f'{log_info_table}的所有者统计.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['排名', 'owner', '数量', '百分比'])

    total_count = sum(row[1] for row in results)

    for i, row in enumerate(results, 1):
        owner = row[0]
        count = row[1]
        percentage = (count / total_count) * 100
        writer.writerow([i, owner, count, f'{percentage:.2f}%'])
    input(f"文件已经在{log_info_table}的所有者统计.csv中，按任意键退出")