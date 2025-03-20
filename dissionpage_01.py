
# from DrissionPage import ChromiumPage
#
# page = ChromiumPage()
# page.get('https://zx.500.com/zc/')
# page.ele('#duizhen_sel')('24085')   # 使用 CSS 角色选择器定位下拉菜单
# # select_element.select('24085')
#
# # 查找表格元素
# items = page.ele('#duizhen_tb')
#
# if items:
#     print('找到了。')
#     p_list = items.eles('a')
#     # 遍历元素并打印<a>元素文本和href属性
#     for item in p_list:
#         print(item.text, item.attr('href'))
# else:
#     print('没有找到。')
#
# # 关闭浏览器
# page.close()

title=['场次', '联赛', '开赛时间', '对阵', '数据', '平均赔率', '选号区\n胜\t平\t负', '选号区', '全包']
from DrissionPage import SessionPage
from DrissionPage import ChromiumPage,ChromiumOptions
from DataRecorder import Recorder
from threading import Thread
from DataRecorder import Filler
from DataRecorder.style import CellStyle
import numpy as np
class Config:
    url = 'https://zx.500.com/zc/'
    port = 7878
    表头 = 'x://*[@id="duizhen_th"]'


# -创建配置对象
co = ChromiumOptions(Config.url)
# -启动配置
co.set_local_port(Config.port)  # 设置本地调试端口# c.ignore certificate_errors(True)
# -创建浏览器
page = ChromiumPage(co)
# page = ChromiumPage()
# tab = page.new_tab()  # 新建标签页，获取标签页对象
page.get(Config.url)
# -创建标签页
f = Recorder(path=r"./dq_sz.xlsx", cache_size=500)
# f.set_table('sheet1')
f.set.head(title)
for str in ["24086","24087"]:
    print(str)
    page('#duizhen_sel')(str).click()
    #获得析，亚，欧的网址
    urls_析=[item.attr('href') for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[5]/a[1]')]
    urls_亚 = [item.attr('href') for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[5]/a[2]')]
    urls_欧 = [item.attr('href') for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[5]/a[3]')]
    shaishi= [item.text for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[2]')]
    url_order=[item.text for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[1]')]
    game_date = [item.text for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[3]')]
    td4_all =np.array([item.text for item in page.eles('x://*[@id="duizhen_tb"]/tr/td[4]/*')]).reshape(14, 5)
    zhudui_scored_all = []
    kedui_scored_all = []
    zhudui_paiming = []
    kedui_paiming = []
    zhudui_names = []
    kedui_names = []
    # for item in scored_all:
    for item in td4_all:
        # 可以在这里增加主队排名，主队名称，客队名称，客队排名
        if "VS" in item:
            zhudui_scored_all.append(-1)
            kedui_scored_all.append(-1)
        else:
            parts = item[2].split(':')  #######################20240514
            # parts = item.replace('[]',"")
            zhudui_scored_all.append(int(parts[0]))
            kedui_scored_all.append(int(parts[1]))
        # print("item=",item)
        if item[0] == "":
            zhudui_paiming.append(-1)
        elif (item[0] is not []):
            zhudui_paiming.append(int(item[0].replace('[', '').replace(']', '')))
        else:
            zhudui_paiming.append(-1)

        if item[0] == "":
            kedui_paiming.append(-1)
        elif item[4] is not []:
            kedui_paiming.append(int(item[4].replace('[', '').replace(']', '')))
        else:
            kedui_paiming.append(-1)

        zhudui_names.append(item[1].replace("\xa0", ""))
        # zhudui_names.append(item[1].replace("\xa0", ""))
        kedui_names.append(item[3].replace("\xa0", ""))

htmls_total = pd.DataFrame(
    {"shaishi": shaishi, "game_date": game_date, "url_order": url_order, "zhudui_paiming": zhudui_paiming,
     "zhudui_name": zhudui_names,
     "zhudui_scored_all": zhudui_scored_all, "kedui_scored_all": kedui_scored_all, "kedui_name": kedui_names,
     "kedui_paiming": kedui_paiming,
     "ouzhi_urls": urls_欧, "yazhi_urls": urls_亚, "shuju_urls": urls_析, "touzhu_urls": htmls_投注})

    tr_list = page.ele('x://*[@id="duizhen_div"]/table/tbody').eles('t:tr')
    table_all=[]
    for tr in tr_list:
        td_list = []
        for td in tr.eles('t:td'):
            urls = [t.text for t in tr.eles('t:td').next(5)]
            shaishi = [t.text for t in tr.eles('t:td')][1]
            game_date = [t.text for t in tr.eles('t:td')][2]
            td_list.append(td.text)
            # print(td_list)

            table_all.append(td_list)
    # print(table_all)
        f.add_data(td_list)
    f.record()


# f.close()
page.close()
