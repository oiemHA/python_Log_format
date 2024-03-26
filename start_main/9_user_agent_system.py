import csv
from collections import defaultdict
import mysql.connector
systems = ['AIX', 'Alpine Linux', 'AmigaOS', 'Android', 'Android Auto', 'Android Go',
           'Android Pie', 'Android Q', 'Android R', 'Android S', 'Android TV', 'Android Wear',
           'Arch Linux', 'Bada', 'BeOS', 'BlackBerry', 'BlackBerry OS', 'Bodhi Linux', 'CentOS',
           'Chrome OS', 'Debian', 'Elementary OS', 'Fedora', 'Firefox OS', 'FreeBSD', 'Gentoo',
           'HP-UX', 'Haiku', 'IRIX', 'KDE neon', 'KaOS', 'KaiOS', 'KaiOSWindows', 'Kali Linux',
           'Kindle', 'Kubuntu', 'Linux', 'Lubuntu', 'MX Linux',  'Mac OS X', 'Mac Os',
           'Macintosh', 'Manjaro', 'Mint', 'MorphOS', 'NetBSD', 'Nintendo', 'Nintendo Wii',
           'Nokia', 'OS/2', 'OpenBSD', 'Palm OS', 'Parrot OS', 'PlayStation', 'Q4OS', 'QNX',
           'RISC OS', 'Raspberry Pi OS', 'Red Hat', 'Roku', 'SUSE', 'Sailfish OS', 'SmartTV',
           'Solaris', 'Solus', 'SolusOS', 'SteamOS', 'SunOS', 'Symbian', 'Tails', 'Tizen',
           'Trisquel', 'Ubuntu', 'Unix', 'Void Linux', 'WebTV',  'Windows 10 Mobile',
           'Windows 11', 'Windows 2000', 'Windows 3.11', 'Windows 7', 'Windows 8', 'Windows 8.1',
           'Windows 95', 'Windows 98', 'Windows CE', 'Windows ME', 'Windows Millennium',
           'Windows Mobile',  'Windows NT 10.0', 'Windows NT 3.1', 'Windows NT 3.5',
           'Windows NT 3.51', 'Windows NT 4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2',
           'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Windows NT 6.3', 'Windows Phone',
           'Windows RT', 'Windows Server', 'Windows Vista', 'Windows XP', 'Xbox', 'Xubuntu', 'Zorin OS',
           'iOS', 'iPadOS', 'macOS', 'macOS Big Sur', 'macOS Catalina', 'macOS High Sierra', 'macOS Mojave',
           'macOS Monterey', 'macOS Sierra', 'macOS Ventura', 'openSUSE', 'tvOS', 'watchOS', 'webOS']

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

query = f"SELECT user_agent, COUNT(*) AS count FROM {log_info_table} GROUP BY user_agent"
cursor.execute(query)

results = cursor.fetchall()

cursor.close()
connection.close()

system_data = defaultdict(int)
total_count = 0

for row in results:
    user_agent = row[0]
    count = row[1]
    total_count += count

    # 提取系统名
    found_systems = []
    for system in systems:
        if system.lower() in user_agent.lower():
            found_systems.append(system)

    if found_systems:
        for system in found_systems:
            system_data[system] += count

# 计算百分比
processed_data = []
for system in systems:
    count = system_data[system]
    percentage = (count / total_count) * 100
    processed_data.append((system, count, f"{percentage:.3f}%"))

# 按数量进行排序
processed_data.sort(key=lambda x: x[1], reverse=True)


with open(f'{log_info_table}的user_agent系统统计.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['排名', '系统名', '数量', '百分比'])

    for i, row in enumerate(processed_data, 1):
        system = row[0]
        count = row[1]
        percentage = row[2]
        writer.writerow([i, system, count, percentage])
input(f"文件{log_info_table}的user_agent系统统计.csv已生成")
