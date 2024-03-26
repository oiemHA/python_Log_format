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
country_rank = input("输入需要排行数/回车排出前十：") or 10

query = f"SELECT country, COUNT(*) AS count FROM {log_info_table} WHERE country IS NOT NULL GROUP BY country ORDER BY count DESC LIMIT {country_rank}"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

countries = [row[0] for row in results]
counts = [row[1] for row in results]

total_count = sum(counts)
percentages = [(count / total_count) * 100 for count in counts]

plt.rcParams['font.sans-serif'] = ['KaiTi']  # 设置字体
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink']
bars = ax.bar(range(len(countries)), counts, color=colors)

for i, bar in enumerate(bars):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    percentage = percentages[i]
    ax.text(x, y, f"{countries[i]}\n{counts[i]}\n{percentage:.2f}%", ha='center', va='bottom')

ax.set_xticks(range(len(countries)))
ax.set_xticklabels(countries, rotation=45, ha='right')

plt.title('国家统计')
plt.xlabel('国家')
plt.ylabel('数量')

plt.savefig(f'{log_info_table}的国家统计.png', dpi=300, bbox_inches='tight')

plt.show()