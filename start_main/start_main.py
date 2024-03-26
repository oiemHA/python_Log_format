import subprocess

print("""Z站长日志处理工具1.0 感谢您的使用,希望能够帮到您!\n网址：https://zzhanzhang.top 作者：娄南湘先生""")

options = {
    "l1": "Log_format_csv.py",
    "l2": "Log_format_DB.py",
    "1": "1_ip_count_csv.py",
    "2": "2_count_cont_txt.py",
    "3": "3_country_count.py",
    "4": "4_city_count.py",
    "5": "5_owner_count_txt.py",
    "6": "6_request_lint_count.py",
    "7": "7_user_agent_Bot_csv.py",
    "8": "8_user_agent_browser_csv.py",
    "9": "9_user_agent_system.py",
    "10": "10_status_code_png.py",
}

while True:
    print("[l1]格式化日志为csv")
    print("[l2]格式化日志为mysql数据表")
    print("[1]ip统计排行")
    print("[2]大洲统计排行")
    print("[3]国家统计排行")
    print("[4]城市统计排行")
    print("[5]ip所有者统计排行")
    print("[6]请求行统计排行")
    print("[7]户代理信息浏览器统计")
    print("[8]用户代理信息机器人统计")
    print("[9]用户代理信息系统统计")
    print("[10]状态码统计")
    print("[q]退出")

    choice = input("输入你的选择：")

    if choice == "q" or choice == "Q":
        break

    if choice not in options:
        print("无效的选择，请重新输入。")
        continue

    script_name = options[choice]
    try:
        subprocess.run(["python", script_name])
    except FileNotFoundError as e:
        print("脚本文件不存在:{}".format(e))
    except subprocess.SubprocessError as e:
        print("执行脚本文件时出现错误:{}".format(e))
