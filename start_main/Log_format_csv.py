# coding: UTF-8
"""
@IDE     ：PyCharm 
@Author  ：娄南湘先生
@Date    ：2024/3/19,0019 18:53 
"""
import csv
import requests
import re
import time as tm
import sys

DEFAULT_API_URL = "https://qifu.baidu.com/ip/geo/v1/district?ip="


def query_ip_location(ip, url_input=None):
    url = url_input if url_input else DEFAULT_API_URL + ip
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Success":
                return data["data"]
    except Exception as e:
        print(f"查询 IP 时出错 {ip}: {e}")
    return None


def parse_log_line(line):
    pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?\[(?P<time>.*?)\]\s*"(?P<method>\w+)\s*(?P<path>.*?)\s*(?P<protocol>.*?)"\s*(?P<status>\d+)\s*(?P<size>\d+)\s*"(?P<referrer>.*?)"\s*"(?P<user_agent>.*?)"'
    match = re.match(pattern, line)
    if match:
        groups = match.groupdict()
        ip = groups['ip']
        time = groups['time']
        method = groups['method']
        path = groups['protocol'].split()[0]
        protocol = groups['protocol'].split()[-1]
        status = groups['status']
        size = groups['size']
        referrer = groups['referrer']
        user_agent = groups['user_agent']

        return ip, time, method, path, protocol, status, size, referrer, user_agent
    return None


def write_to_csv(log_data, filename):
    headers = ["ip", "大洲", "国家", "城市", "城市编码", "经度", "纬度", "所有者", "运营商", "请求时间", "请求方法",
               "请求行", "请求的资源路径", "HTTP协议版本", "状态码+描述", "响应大小", "引用页", "用户代理信息"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for entry in log_data:
            writer.writerow(entry)


def main():
    log_filename = input("把日志文件拖过来：")
    # log_filename = "../zzhanzhang.top.log"  # 测试
    ip_locations = {}
    log_data = []
    # 如果日志的行数超过1W条，只读取最后1W行,y和n选项来是否继续,y选择从最后1w行处理,n选项处理全部的日志,或者输入数字从指定行数开始处理
    with open(log_filename, mode='r', encoding='utf-8') as file:
        line_count = sum(1 for _ in file)
        if line_count >= 10000:
            choice = input(
                f"该日志行数超过1W条，共有{line_count}行，是否只处理最后1W条(y/n), 或输入数字从指定行数开始处理: ")
            if choice.lower() == "y":
                file.seek(0)
                lines_to_skip = max(0, line_count - 10000)
                for _ in range(lines_to_skip):
                    next(file)
            elif choice.isdigit():
                start_line = int(choice)
                file.seek(0)
                for _ in range(start_line):
                    next(file)
            else:
                file.seek(0)

        start_time = tm.time()
        loading_symbols = ['| ', '- ', '/ ', '\\ ']
        loading_index = 0
        for idx, line in enumerate(file):
            parsed_line = parse_log_line(line)
            if parsed_line:
                ip, time, method, path, xie_yi, status, size, referrer, user_agent = parsed_line
                if ip not in ip_locations:
                    ip_location = query_ip_location(ip)
                    if ip_location:
                        ip_locations[ip] = ip_location
                else:
                    ip_location = ip_locations[ip]

                if ip_location:
                    entry = {
                        "ip": ip,
                        "大洲": ip_location.get("continent", "null"),
                        "国家": ip_location.get("country", "null"),
                        "城市": ip_location.get("city", "null"),
                        "城市编码": ip_location.get("areacode", "null"),
                        "经度": ip_location.get("lng", "null"),
                        "纬度": ip_location.get("lat", "null"),
                        "所有者": ip_location.get("owner", "null"),
                        "运营商": ip_location.get("isp", "null"),
                        "请求时间": time,
                        "请求方法": method,
                        "请求行": f"{method} {path} {xie_yi}",

                        "请求的资源路径": path,
                        "HTTP协议版本": xie_yi,
                        "状态码+描述": status + ("部分成功" if 100 <= int(status) < 200 else "成功" if 200 <= int(
                            status) < 300 else "细化请求" if 300 <= int(status) < 400 else "客户端错误" if 400 <= int(
                            status) < 500 else "服务器错误"),
                        "响应大小": size,
                        "引用页": referrer,
                        "用户代理信息": user_agent
                    }
                    # print(entry)
                    log_data.append(entry)

            # # 显示加载进度
            sys.stdout.write(f"\r格式化中 {loading_symbols[loading_index]}")
            loading_index = (loading_index + 1) % len(loading_symbols)
            sys.stdout.flush()

    write_to_csv(log_data, f"{log_filename}已处理.csv")
    end_time = tm.time()
    print(f"\nIP属地查询完成,日志格式化完成,TIME: {end_time - start_time:.1f}S,文件保存在{log_filename}已处理.csv")


if __name__ == "__main__":
    main()
