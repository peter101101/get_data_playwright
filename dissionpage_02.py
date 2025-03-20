
from DrissionPage import SessionPage
from DrissionPage import ChromiumPage,ChromiumOptions
from DataRecorder import Recorder
from threading import Thread
from DataRecorder import Filler
from DataRecorder.style import CellStyle
import numpy as np
import re
import pandas as pd
def get_haoma(html_xi):
    """
    从网址中提取数字号码
    :param html_xi:网址
    :return: 匹配的号码
    """
    haoma = []
    pattern = re.compile(r'\d+(?=\.\w+$)')
    for url in html_xi:
        match = pattern.search(url)
        if match:
            # print(match.group())
            haoma.append(match.group())
    return haoma
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
# f.set.head(title)


for str in ["24086","24087"]:
    print(str)
    page('#duizhen_sel')(str).click()
    tr_list = page.ele('x://*[@id="duizhen_div"]/table/tbody').eles('t:tr')
    table_all=[]
    for tr in tr_list:
        td_list = []
        # for td in tr.eles('t:td'):
        urls = [t.attr('href')  for t in tr.eles('x:/td[5]/a[1]')]
        haoma = get_haoma(urls)
        htmls_数据 = [('http://odds.500.com' + '/fenxi/shuju-' + i + '.shtml') for i in haoma]
        htmls_投注 = [('http://odds.500.com' + '/fenxi/touzhu-' + i + '.shtml') for i in haoma]
        htmls_欧赔 = [('http://odds.500.com' + '/fenxi/ouzhi-' + i + '.shtml') for i in haoma]
        htmls_亚赔 = [('http://odds.500.com' + '/fenxi/yazhi-' + i + '.shtml') for i in haoma]
        url_order = [item.text for item in tr.eles('x:/td')][0]
        zhudui_names=[item.text.replace("\xa0", "") for item in tr.eles('x:/td[4]/*')][1]
        # zhudui_names.append(item[1].replace("\xa0", ""))
        kedui_names=[item.text.replace("\xa0", "") for item in tr.eles('x:/td[4]/*')][3]

        shaishi = [t.text for t in tr.eles('t:td')][1]
        game_date = [t.text for t in tr.eles('t:td')][2]

        # td4_all = np.array([item.text for item in tr.eles('x:/td[4]/i[2]')])
        xpath_result = [item.text for item in tr.eles('x:/td[4]/i')]

        # zhudui_scored_all = ["-1:-1"] if "VS" in xpath_result else []
        if ("VS" in xpath_result):
            if "VS" in xpath_result:
                zhudui_scored=-1
                kedui_scored=-1
            else:
                parts = xpath_result[2].split(':')  #######################20240514
                # parts = item.replace('[]',"")
                zhudui_scored=int(parts[0])
                kedui_scored=int(parts[1])
            zhudui_paiming_temp = [item.text for item in tr.eles('x:/td[4]/i[1]')]
            zhudui_paiming = [-1 if item == '' else int(item.strip('[]')) if item.strip('[]').isdigit() else -1 for item
                              in zhudui_paiming_temp]


        kedui_paiming_temp = [item.text for item in tr.eles('x:/td[4]/i[2]')]
        kedui_paiming = [-1 if item == '' else int(item.strip('[]')) if item.strip('[]').isdigit() else -1 for item
                                 in kedui_paiming_temp]
        data_total ={
            "shaishi": shaishi, "game_date": game_date, "url_order": url_order,
            "zhudui_paiming": zhudui_paiming,"zhudui_name": zhudui_names,
            "zhudui_scored": zhudui_scored, "kedui_scored": kedui_scored,
            "kedui_name": kedui_names,
            "kedui_paiming": kedui_paiming,
            "ouzhi_urls": htmls_欧赔, "yazhi_urls": htmls_亚赔,
            "shuju_urls": htmls_数据, "touzhu_urls": htmls_投注}
        print(f'datas={data_total}')

        # ou_data=run_ou()
        # td_list.append(td.text)
            # print(td_list)

            # table_all.append(td_list)
    # # print(table_all)
        f.add_data(data_total)
        f.record()
# f.close()
page.close()

