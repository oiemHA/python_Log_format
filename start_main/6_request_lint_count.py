import mysql.connector
import pandas as pd

def connect_to_database(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print(f"连接数据库失败: {err}")
        return None


def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = cursor.column_names
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        return df
    except mysql.connector.Error as err:
        print(f"执行查询失败: {err}")
        return None
def save_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        input(f"结果已保存为 {filename}")
    except Exception as e:
        print(f"保存CSV文件失败: {e}")


def main():
    mysql_host = input("数据库地址(回车为localhost本地数据库)：") or "localhost"
    mysql_user = input("数据库用户：")
    mysql_pwd = input("数据库密码：")
    mysql_db = input("数据库名或者回车使用默认(Log_format_DB.py自动创建的库)：") or "log_info_db"
    log_info_table = input("输入表名或者回车使用默认(为Log_format_DB.py自动创建的表)：") or "log_data_table"
    request_rank = input("输入需要排行数/回车排出前十：") or 10
    if_owner = input("是否关联owner（y/n）：")

    if if_owner.lower() == "y":
        query = f"""
        SELECT request_line, GROUP_CONCAT(owner SEPARATOR ', ') AS owners, COUNT(*) AS count,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {log_info_table}) AS percentage
        FROM {log_info_table}
        GROUP BY request_line
        ORDER BY count DESC
        LIMIT {request_rank}
        """
    else:
        query = f"""
        SELECT request_line, COUNT(*) AS count,
               COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {log_info_table}) AS percentage
        FROM {log_info_table}
        GROUP BY request_line
        ORDER BY count DESC
        LIMIT {request_rank}
        """

    connection = connect_to_database(mysql_host, mysql_user, mysql_pwd, mysql_db)
    if connection is None:
        return
    df = execute_query(connection, query)
    if df is None:
        connection.close()
        return
    filename = f"{log_info_table}的request_line请求行统计.csv"
    save_to_csv(df, filename)
    connection.close()


if __name__ == "__main__":
    main()
