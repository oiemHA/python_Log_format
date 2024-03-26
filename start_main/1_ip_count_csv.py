import csv
import mysql.connector

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
ip_rank = input("输入需要排行数/回车排出前十：") or 10

query = f"SELECT ip, country, city, owner, COUNT(*) AS count FROM {log_info_table} GROUP BY ip ORDER BY count DESC LIMIT {ip_rank}"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

with open(f'{log_info_table}的ip统计.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['排名', 'ip', 'country', 'city', 'owner', '数量', '百分比'])

    total_count = sum(row[4] for row in results)  # 计算总数量

    for index, row in enumerate(results, 1):
        ip, country, city, owner, count = row
        percentage = "{:.2f}".format((count / total_count) * 100)
        writer.writerow([index, ip, country, city, owner, count, percentage])
input(f"{log_info_table}的ip统计.csv文件已成功生成,任意键退出")
