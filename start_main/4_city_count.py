import matplotlib.pyplot as plt
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
city_rank = input("输入需要排行数/回车排出前十：") or 10

query = f"SELECT city, COUNT(*) AS count FROM {log_info_table} WHERE city IS NOT NULL GROUP BY city ORDER BY count DESC LIMIT {city_rank}"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

cities = [row[0] for row in results]
counts = [row[1] for row in results]

total_count = sum(counts)
percentages = [(count / total_count) * 100 for count in counts]

plt.rcParams['font.sans-serif'] = ['KaiTi']

fig, ax = plt.subplots(figsize=(10, 8))
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink',
          'lightblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightpink', 'lightgray', 'lightyellow',
          'lightskyblue', 'lightseagreen', 'lightsteelblue']
bars = ax.barh(range(len(cities)), counts, color=colors)

for i, bar in enumerate(bars):
    x = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    percentage = percentages[i]
    ax.text(x, y, f"{counts[i]}\n{percentage:.2f}%", ha='left', va='center')

ax.set_yticks(range(len(cities)))
ax.set_yticklabels(cities)

plt.title('地区统计')
plt.xlabel('数量')
plt.ylabel('地区')

plt.savefig(f'{log_info_table}的地区统计.png', dpi=300, bbox_inches='tight')

plt.show()