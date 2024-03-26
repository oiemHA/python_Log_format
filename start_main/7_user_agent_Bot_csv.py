# coding: UTF-8
"""
@IDE     ：PyCharm 
@Author  ：娄南湘先生
@Date    ：2024/3/22,0022 15:16 
"""
import csv
from collections import defaultdict
import mysql.connector

# 机器人名列表
robots = [
    "Googlebot", "Bingbot", "Yahoo", "Slurp", "Baiduspider", "YandexBot", "DuckDuckBot",
    "Sogou web spider", "Exabot", "FacebookBot", "Twitterbot", "LinkedInBot", "Pinterestbot",
    "Applebot", "MJ12bot", "AhrefsBot", "SemrushBot", "RamblerBot", "DotBot", "BingPreview",
    "YandexImages", "Screaming Frog SEO Spider", "SeznamBot", "Embedly", "Slackbot", "TelegramBot",
    "WhatsApp", "Discordbot", "360Spider", "MSNBOT", "NaverBot", "Gigabot", "YandexMobileBot",
    "FacebookExternalHit", "Pinterest", "Ask Jeeves/Teoma", "Alexa Crawler",
    "YodaoBot", "ia_archiver",
    "CoccocBot", "Vsekorakhiver", "voilabot", "mail.ru_bot", "NZZ3", "TurnitinBot",
    "ScopeusBot", "GrapeshotCrawler", "Curalab", "SiteBot", "SitebeamBot", "SEOstats Crawler",
    "Butterfly Collector", "Genieo Web filter",
    "InfoSeek Robot 1.0", "W3 SiteSearch Crawler", "ZoomSpider.net", "Ezooms", "Teoma",
    "Scooter", "WebAlta Crawler", "Gigabot", "Alexa Media Crawler",
    "MojeekBot", "BLEXBot", "YandexSomething", "CrawllyBot",
    "Wotbox", "SiteExplorer.com",
    "sogou spider", "sogou news spider", "sogou orion spider", "sogou pic spider", "sogou video spider"
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

robot_data = defaultdict(int)
total_count = 0

for row in results:
    user_agent = row[0]
    count = row[1]
    total_count += count

    found_robots = []
    for robot in robots:
        if robot.lower() in user_agent.lower():
            found_robots.append(robot)

    if found_robots:
        for robot in found_robots:
            robot_data[robot] += count

processed_data = []
for robot in robots:
    count = robot_data[robot]
    percentage = (count / total_count) * 100
    processed_data.append((robot, count, f"{percentage:.4f}%"))

processed_data.sort(key=lambda x: x[1], reverse=True)

with open(f'{log_info_table}的user_agent机器人统计.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['排名', '机器人名', '数量', '百分比'])

    for i, row in enumerate(processed_data, 1):
        robot = row[0]
        count = row[1]
        percentage = row[2]
        writer.writerow([i, robot, count, percentage])
input(f"文件{log_info_table}的user_agent机器人统计.csv已生成")
