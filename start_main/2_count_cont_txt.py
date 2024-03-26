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

query = f"SELECT continent, COUNT(*) AS count FROM {log_info_table} WHERE continent IS NOT NULL GROUP BY continent"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

continents = [row[0] for row in results]
counts = [row[1] for row in results]

total_count = sum(counts)
percentages = [(count / total_count) * 100 for count in counts]

lines = [f"{continent} {count} {percentage:.2f}%" for continent, count, percentage in
         zip(continents, counts, percentages)]
output = '\n'.join(lines)

with open(f'{log_info_table}大洲统计.txt', 'w') as file:
    file.write(output)
input(f"{log_info_table}的大洲统计.txt文件已成功生成，任意键退出")
