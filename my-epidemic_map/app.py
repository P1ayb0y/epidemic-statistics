from flask import Flask
from flask import request
from flask import render_template
from jieba.analyse import extract_tags
from flask import jsonify
import string
import utils


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("main.html")


@app.route("/time")
def get_time():
    return utils.get_time()

@app.route("/c1")
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm":data[0],"nowconfirm":data[1],"supect":data[2], "heal":data[3], "dead":data[4]})

@app.route("/c2")
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm, heal, dead = [],[],[],[]
    for a,b,c,d in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        heal.append(c)
        dead.append(d)
    return jsonify({"day":day,"confirm":confirm,"heal":heal,"dead":dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day, nowconfirm, suspect, confirm_add, suspect_add = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d"))
        nowconfirm.append(b)
        suspect.append(c)
        confirm_add.append(d)
        suspect_add.append(e)
    return jsonify({"day":day,"nowconfirm":nowconfirm,"suspect":suspect,"confirm_add":confirm_add,"suspect_add":suspect_add})



@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    count = []
    count.append(['province', '本日新增', '现有确诊'])
    for a, b, c in data:
        count1 = []
        count1.append(a)
        count1.append(int(b))
        count1.append(int(c))
        count.append(list(count1))
    print(count)
    return jsonify({"data":count})

@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits) #移除热搜数字
        v = i[0][len(k)]    #获取热搜数字
        ks = extract_tags(k)    #使用jieba提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name":j,"value":v})
    return jsonify({"kws":d})



if __name__ == '__main__':
    app.run()


