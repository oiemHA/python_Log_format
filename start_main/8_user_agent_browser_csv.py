import re
import mysql.connector
import csv
from collections import defaultdict

browsers = [
    "Chrome", "Safari", "Firefox", "Internet Explorer", "Edge", "Edg", "Opera", "Brave", "BIDUBrowser",
    "UCBrowser", "SamsungBrowser", "Maxthon", "Netscape", "Konqueror", "SeaMonkey", "Camino", "MSIE",
    "PaleMoon", "Waterfox", "Vivaldi", "Avant Browser", "Yandex", "Epic Privacy Browser", "Torch",
    "SlimBrowser", "Midori", "Dolphin", "Puffin", "Silk", "BlackBerry", "IE Mobile", "Android Browser",
    "Chrome Mobile", "Opera Mini", "UCWEB", "QQBrowser", "QQ", "Tor Browser",
    "Comodo Dragon", "Sogou Explorer", "360 Browser", "Baidu Browser", "Samsung Internet", "Opera Coast",
    "Opera GX", "Brave Mobile", "Firefox Focus", "Firefox Reality", "Microsoft Internet Explorer",
    "Microsoft Edge Mobile", "Chromium", "Seamonkey", "K-Meleon", "Avast Secure Browser", "Bitwarden Authenticator",
    "Brave Shields", "Brave Rewards", "CentBrowser", "Coc Coc", "Comodo IceDragon", "Disruptor Browser",
    "GreenBrowser", "Iridium Browser", "K-Ninja", "Kiwi Browser", "Lunascape", "Maxthon Cloud Browser",
    "Orbitum", "QupZilla", "Slimjet", "SRWare Iron", "Torch Browser", "UCWeb Browser", "Vivaldi Snapshot",
    "Xombrero", "Opera GX Gaming Browser", "Opera Touch", "Brave Browser for Android", "Firefox for Android",
    "Chrome for Android", "Edge for Android", "Samsung Internet for Android", "UC Browser for Android",
    "QQ Browser for Android", "Brave Browser for iOS", "Firefox for iOS", "Safari for iOS", "Opera for iOS",
    "Opera Coast for iOS", "Puffin Browser", "Dolphin Browser", "CM Browser", "Flynx Browser", "Ghostery Browser",
    "Maxthon Browser", "Opera Mini for Windows", "Perfect Browser", "Photon Browser"
]

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

browser_data = defaultdict(int)
total_count = 0

for row in results:
    user_agent = row[0]
    count = row[1]
    total_count += count

    found_browsers = []
    for browser in browsers:
        if re.search(r'\b' + re.escape(browser) + r'\b', user_agent, flags=re.IGNORECASE):
            found_browsers.append(browser)

    if found_browsers:
        for browser in found_browsers:
            browser_data[browser] += count


processed_data = []
for browser in browsers:
    count = browser_data[browser]
    percentage = (count / total_count) * 100
    processed_data.append((browser, count, f"{percentage:.4f}%"))


processed_data.sort(key=lambda x: x[1], reverse=True)

with open(f'{log_info_table}的user_agent浏览器统计.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['排名', '浏览器名', '数量', '百分比'])

    for i, row in enumerate(processed_data, 1):
        browser = row[0]
        count = row[1]
        percentage = row[2]
        writer.writerow([i, browser, count, percentage])
input(f"文件{log_info_table}的user_agent浏览器统计.csv已生成")
