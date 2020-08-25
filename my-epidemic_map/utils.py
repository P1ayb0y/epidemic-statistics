import time
import pymysql
import string
from jieba.analyse import extract_tags

def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X").format("年","月","日")
    return time_str


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

def query(sql,*args):
    """

    封装通用查询方法
    :param sql:
    :param args:
    :return: 返回查询结果（（），（））的形式
    """

    conn, cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def get_c1_data():
    """
    :return:大屏数据
    """
    sql = "select confirm,nowconfirm,supect,heal,dead from history order by ds desc "
    conn, cursor = get_conn()
    cursor.execute(sql)
    res = cursor.fetchone()
    close_conn(conn, cursor)
    return res


def get_c2_data():
    """

    :return:地图数据
    """
    #因为会多次更新数据区时间戳最新的
    sql = "select province,sum(nowconfirm) from details where update_time=(\
            select update_time from details order by update_time desc limit 1) group by province"
    res = query(sql)
    return res

def get_l1_data():
    """
    获取左上角疫情累计曲线图数据
    :return: 确诊，治愈，死亡
    """

    sql = "select ds,confirm,heal,dead from history"
    res = query(sql)
    return res

# def get_l2_data():
#     sql = "select ds,confirm,heal,dead from history"
#     res = query(sql)
#     return res

def get_l2_data():
    """
    获取左下角曲线图数据
    """
    sql = "select ds,nowconfirm,supect,confirm_add,supect_add from history"
    res = query(sql)
    return res

def get_r1_data():
    """
    获取今日全国疫情最严重地区数据
    :return:
    """
    sql = "select province,sum(confirm_add),sum(nowconfirm) from details where update_time=(\
            select update_time from details order by update_time desc limit 1) group by province"
    res = query(sql)
    new_list1 = []
    new_list2 = []
    for item in res:
        new_list1.append(item[::-1])
    new_list1 = sorted(new_list1, reverse=True)
    for item in new_list1:
        new_list2.append(item[::-1])
    return new_list2[0:5:1]

def get_r2_data():
    """
    获取词云图数据
    :return: 最近20条热搜
    """
    sql = "select content from hotsearch order by id desc limit 20"
    res = query(sql)
    return res


if __name__ == "__main__":
    # print(get_time())
    # print(get_c1_data())
    # print(get_c2_data())
    # print(get_l1_data())
    print(get_r1_data())
    # count, count1 = [], []
    # count.append(['date', '累计确诊', '治愈', '死亡'])
    # for a, b, c, d in get_l1_data():
    #     count1.append(a.strftime("%m-%d"))
    #     count1.append(b)
    #     count1.append(c)
    #     count1.append(d)
    #     count.append(list(count1))
    # print(count)

