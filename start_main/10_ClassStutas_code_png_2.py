# coding: UTF-8
"""
@IDE     ：PyCharm 
@Author  ：娄南湘先生
@Date    ：2024/3/22,0022 17:11 
"""
import pymysql
import matplotlib.pyplot as plt

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='log_info_ip_data'
)

cursor = connection.cursor()

query = "SELECT status_code, COUNT(*) AS count FROM log_data_20240321_tail_1w GROUP BY status_code"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

# 响应状态字典
status_dict = {
    "1xx": "部分成功",
    "2xx": "成功",
    "3xx": "细化请求",
    "4xx": "客户端错误",
    "5xx": "服务器错误",
    "other": "其他"
}

# 统计状态数量
status_data = {}
total_count = 0

for row in results:
    status_code = row[0]
    count = row[1]
    total_count += count

    # 根据状态码判断所属状态
    if status_code.startswith("1"):
        status_data.setdefault("1xx", 0)
        status_data["1xx"] += count
    elif status_code.startswith("2"):
        status_data.setdefault("2xx", 0)
        status_data["2xx"] += count
    elif status_code.startswith("3"):
        status_data.setdefault("3xx", 0)
        status_data["3xx"] += count
    elif status_code.startswith("4"):
        status_data.setdefault("4xx", 0)
        status_data["4xx"] += count
    elif status_code.startswith("5"):
        status_data.setdefault("5xx", 0)
        status_data["5xx"] += count
    else:
        status_data.setdefault("other", 0)
        status_data["other"] += count

plt.rcParams['font.sans-serif'] = ['SimHei']
labels = []
sizes = []
percentages = []

for status, count in status_data.items():
    labels.append(f"{status_dict[status]} ({count})")
    sizes.append(count)
    percentage = (count / total_count) * 100
    percentages.append(percentage)

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.3f%%', startangle=90)
ax.axis('equal')

plt.title('响应状态统计')

plt.savefig('响应状态统计2.png')

plt.show()