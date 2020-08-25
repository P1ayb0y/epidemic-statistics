import json
import requests
import pymysql
import time
import traceback
import asyncio
from selenium.webdriver import Chrome,ChromeOptions
import sys

def get_tencent_data():
    """
    :爬取腾讯疫情的历史数据和每日数据
    """

    user = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4170.0 Safari/537.36 Edg/85.0.552.1"
    }
    tencent_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    tencent_url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    res = requests.get(tencent_url, headers=user)
    d = json.loads(res.text)
    data_all = json.loads(d['data'])
    res1 = requests.get(tencent_url1, headers=user)
    d1 = json.loads(res1.text)
    data_all_1 = json.loads(d1['data'])

    history = {}  # 历史数据
    for i in data_all["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        nowconfirm = i["nowConfirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "nowconfirm": nowconfirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []  # 当日新增
    update_time = data_all_1["lastUpdateTime"]
    data_province = data_all_1["areaTree"][0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省份名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            nowconfirm = city_infos["total"]["nowConfirm"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, nowconfirm, heal, dead])
    return history, details


def get_conn():
    """
    创建数据库连接，return：连接和游标
    """
    config = {
        "host": "cdb-g2c8lstc.cd.tencentcdb.com",  # 地址
        "port": 10158,  # 端口
        "user": "root",  # 用户名
        "password": "pb197622",  # 密码
        "database": "cov19",  # 数据库名;如果通过Python操作MySQL,要指定需要操作的数据库
        "charset": "utf8"
    }

    db = pymysql.connect(**config)

    cursor = db.cursor()
    return db, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def update_details():
    """
    更新 details表数据
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1] #0是历史数据字典，1是最新详细数据列表
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,nowconfirm,heal,dead) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select %s=(select update_time from details order by id desc limit 1)" #对比最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已经是最新数据")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_histroy():
    """
    插入历史数据
    ：return ：
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0] #0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k,v in dic.items():
            #item 格式 {'2020-01-13':{'confirm':41',...suspect':0,'dead':1}...}
            cursor.execute(sql,[k,v.get("confirm"),v.get("nowconfirm"),v.get("confirm_add"),v.get("suspect"),\
                              v.get("suspect_add"),v.get("heal"),v.get("heal_add"),\
                              v.get("dead"),v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}插入历史数据完成")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


def update_histroy():
    """
    更新历史数据
    ：return ：
    """
    cursor = None
    conn = None

    try:
        dic = get_tencent_data()[0]  # 0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s "
        for k, v in dic.items():
            # item 格式 {'2020-01-13':{'confirm':41',...suspect':0,'dead':1}...}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("nowconfirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), \
                                     v.get("heal"), v.get("heal_add"), v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"{time.asctime()}更新历史数据完成")

    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def get_baidu_hot():
    """
    :return:返回百度疫情热搜
    """
    url = "https://voice.baidu.com/act/virussearch/virussearch/?from=osari_aladin_news"
    option = ChromeOptions()
    option.add_argument("--headless") #隐藏浏览器
    option.add_argument("--nosandbox")#禁止沙盘
    brower = Chrome(options=option)
    brower.get(url)
    #print(brower.page_source)
    click = brower.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-6_32AY4F.VirusHot_1-5-6_2RnRvg > section > div')
    click.click()#点击展开
    time.sleep(1)
    hot = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')
    context = [i.text for i in hot] #获取标签内容
    print(context)
    return context

def get_xinlang_hot():
    """
    :return:返回百度疫情热搜
    """
    url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
    option = ChromeOptions()
    option.add_argument("--headless") #隐藏浏览器
    option.add_argument("--no-sandbox")#禁止沙盘
    brower = Chrome(options=option)
    brower.get(url)
    #print(brower.page_source)
    time.sleep(1)
    hot = brower.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a')
    value = brower.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/span')
    context1 = [i.text for i in hot] #获取标签内容
    context2 = [j.text for j in value]
    context = []
    for k in range(50):
        text = context1[k]+context2[k]
        context.append(text)
    print(context)
    return context

def update_hotsearch():
    """
    更新疫情热搜词进数据库
    :return:
    """
    cursor = None
    conn = None
    try:
        context = get_xinlang_hot()
        print(f"{time.asctime()}热词数据开始更新")
        conn, cursor = get_conn()
        sql = "insert into hotsearch (dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql,(ts,i))
        conn.commit()
        print(f"{time.asctime()}热词数据更新完成")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

if __name__=="__main__":
    l = len(sys.argv)
    if l == 1:
        s = """
        请输入参数
        参数说明：
        up_his 更新历史记录表
        up_det 更新详细表
        up_hot 更新热搜表
        """
        print(s)

    else:
        order = sys.argv[1]
        if order == "up_his":
            update_histroy()
        elif order == "up_det":
            update_details()
        elif order == "up_hot":
            update_hotsearch()





