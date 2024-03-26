import re
import mysql.connector
import requests
import time
import sys
from fake_useragent import UserAgent

mysql_host = input("请输入数据库地址(回车为localhost本地数据库)：") or "localhost"
mysql_user = input("请输入数据库用户：")
mysql_pwd = input("请输入数据库密码：")

db_connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pwd,
)

db_cursor = db_connection.cursor()

db_cursor.execute("CREATE DATABASE IF NOT EXISTS log_info_db")
db_cursor.execute("USE log_info_db")

create_table_query = """
CREATE TABLE IF NOT EXISTS log_data_table (
    ip TEXT,
    continent TEXT,
    country TEXT,
    city TEXT,
    city_code TEXT,
    longitude TEXT,
    latitude TEXT,
    owner TEXT,
    isp TEXT,
    request_time TEXT,
    request_line LONGTEXT,
    http_version TEXT,
    status_code TEXT,
    response_size TEXT,
    referer LONGTEXT,
    user_agent LONGTEXT
)
"""
db_cursor.execute(create_table_query)

def query_ip_location(ip):
    retry_count = 0
    while retry_count < 3:
        try:
            response = requests.get(f"https://qifu.baidu.com/ip/geo/v1/district?ip={ip}",
                                    headers={'User-Agent': ua.random},
                                    timeout=3)
            if response.status_code == 200:
                data = response.json().get('data', {})
                # print(data)
                # 响应数据完整性
                if all(key in data for key in
                       ['continent', 'country', 'prov', 'city', 'areacode', 'lng', 'lat', 'owner', 'isp']):
                    return (
                        data.get('continent', 'null'),
                        data.get('country', 'null'),
                        f"{data.get('prov', 'null')} {data.get('city', 'null')}" if data.get('prov') or data.get(
                            'city') else 'null',
                        data.get('areacode', 'null'),
                        data.get('lng', 'null'),
                        data.get('lat', 'null'),
                        data.get('owner', 'null'),
                        data.get('isp', 'null')
                    )
                else:
                    # print(f"{ip}数据不完整")
                    retry_count += 1
            elif response.status_code == 429:
                # print(f"429 之后重试 {retry_count * 0.05} 秒。。。")
                time.sleep(retry_count * 0.08)
                retry_count += 1
            else:
                # print(f"{response.status_code}")
                return ('null', 'null', 'null', 'null', 'null', 'null', 'null', 'null')
        except Exception as e:
            # print(f"{ip}: {e}")
            return ('null', 'null', 'null', 'null', 'null', 'null', 'null', 'null')

    # print(f"无法检索完整数据 {ip} 重试 3 次后.")
    return ('null', 'null', 'null', 'null', 'null', 'null', 'null', 'null')

log_file_path = input("把日志文件拖过来：")
# log_file_path = "../zzhanzhang.top.log"
log_entries = []

with open(log_file_path, 'r') as file:
    lines = file.readlines()
    line_count = len(lines)

    if line_count >= 10000:
        choice = input(f"该日志行数超过1W条，共有{line_count}行，[y]处理最后1W条[n]处理全部, 或输入数字从指定行数开始处理: ")
        if choice.lower() == "y":
            lines = lines[-10000:]
        elif choice.isdigit():
            start_line = int(choice)
            lines = lines[max(0, start_line - 1):]

    for line in lines:
        match = re.match(r'^(\S+) - - \[(.+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+) "([^"]+)" "([^"]+)"$', line)
        if match:
            ip, request_time, request_method, request_path, http_version, status_code, response_size, referer, user_agent = match.groups()
            status_code_description = (
                "部分成功" if 100 <= int(status_code) < 200 else
                "成功" if 200 <= int(status_code) < 300 else
                "细化请求" if 300 <= int(status_code) < 400 else
                "客户端错误" if 400 <= int(status_code) < 500 else
                "服务器错误"
            )
            log_entries.append({
                'ip': ip,
                'request_time': request_time,
                'request_line': f"{request_method} {request_path}",
                'http_version': http_version,
                'status_code': status_code + status_code_description,
                'response_size': response_size,
                'referer': referer,
                'user_agent': user_agent
            })

start_time = time.time()
total_entries = len(log_entries)
loading_symbols = ['| ', '- ', '/ ', '\\ ']
loading_index = 0
ua = UserAgent()

for index, entry in enumerate(log_entries):
    ip = entry['ip']

    # 查询IP属地
    continent, country, city, city_code, longitude, latitude, owner, isp = query_ip_location(ip)

    insert_query = """
    INSERT INTO log_data_table (ip, continent, country, city, city_code, longitude, latitude, owner, isp, request_time, 
                          request_line, http_version, status_code, response_size, referer, user_agent) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    db_cursor.execute(insert_query,
                      (ip, continent, country, city, city_code, longitude, latitude, owner, isp, entry['request_time'],
                       entry['request_line'], entry['http_version'], entry['status_code'],
                       entry['response_size'], entry['referer'], entry['user_agent']))
    db_connection.commit()

    # loading
    sys.stdout.write(f"\r格式化中 {loading_symbols[loading_index]}")
    sys.stdout.flush()
    loading_index = (loading_index + 1) % len(loading_symbols)

    # 随机等待
    # time.sleep(random.uniform(0, 0.05))

end_time = time.time()

db_cursor.close()
db_connection.close()

print(f"\nIP属地查询完成, 日志格式化完成,保存在log_info_db数据库中的log_data_table表中\nTIME: {end_time - start_time:.1f}S")
input("任意键继续：")
