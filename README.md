# python_Log_format
2024_03_25娄老师的作业:使用python编写代码对服务器的响应日志进行格式化到数据库或csv并作简要分析

>需求:将日志格式化到mysql数据库中或者csv中,并作简要统计和分析,并使用ip查询api查询ip属地信息；

### 日志文件

>提供了text_log.log样本日志,或者自备;

### ip属地查询

- 是否使用ip属地查询?

  1. 启用(会增加耗时,建议不超过不要超过10万条log信息,查询一万条ip属地信息的时间大概为30分钟左右,使用多线程也可以)查询的数据返回以下内容

    ```json
  {
    "code": "Success",
    "data": {
        "continent": "亚洲",
        "country": "印度尼西亚",
        "zipcode": "",
        "timezone": "UTC+7",
        "accuracy": "省",
        "owner": "Institut Teknologi Del",
        "isp": "Institut Teknologi Del",
        "source": "数据挖掘",
        "areacode": "ID",
        "adcode": "",
        "asnumber": "142367",
        "lat": "2.110200",
        "lng": "99.541564",
        "radius": "",
        "prov": "北苏门答腊省",
        "city": "",
        "district": ""
    },
    "charge": false,
    "msg": "查询成功",
    "ip": "103.167.217.137",
    "coordsys": "WGS84"
    }
    ```

  1. 不启用查询(会很快!几百mb的log秒级处理);
  2. 如果选择保存到数据库中,会创建一个默认的表来保存日志各个信息;

### 项目文件说明

  - start_main.py

    >   所有需求区块的启动脚本,使用编号来选择功能

    ```python
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
    ```

- log_format_csc.py

  >将日志格式化到csv中

- log_format_DB.py

  >将日志格式化到结构化数据表中

- 功能区块一:1_ip_count_csv.py

  > 根据ip来处理,得到数据:"排名,ip,country,city,owner,数量,百分占比"
  > 可自定义选择返回前XX名的ip信息,但是ip属地信息没有被查询的话,country和city和owner就不会返回数据
  > 统计后的数据会保存到ip统计.csv中;

- 功能区块二:2_count_cont_txt.py

  > 统计大洲之间的数量和百分占比

- 功能区块三:3_country_count.py

  > 统计日志的"country"字段的信息,排名,绘制成柱状图显示出来;

- 功能区块四:4_city_count.py

  > 统计日志信息里的"city"字段信息,绘制成柱状图显示出啦

- 功能区块五:5_owner_count_txt.py

  > 统计"owner"字段的ip所有者的信息平排序

- 功能区块六:6_request_lint_count.py

  > 统计请求行的信息,统计X排名前的信息,并统计访问这个链接最多的"owner"信息(供选)

- 功能区块七:7_user_agent_Bot_csv.py

  > 统计"user_agent"字段中的浏览器信息

- 功能区块八:8_user_agent_browser_csv.py

  > 统计"user_agent"字段中的机器人信息

- 功能区块九:9_user_agent_system.py

  >统计"user_agent"字段中的系统信息

- 功能区块10:10_stutas_code_png.py

  > 统计"stutas_code"字段响应状态的信息,分类汇总
  >
  > ***各个.py运行需要保存的文件名字为{库名}+功能名***

 



