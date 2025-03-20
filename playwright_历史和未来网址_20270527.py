from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
from datetime import datetime
import random
import numpy as np
import re

def yapei_handle(ls):
    """
    :param ls: 输入亚赔的list
    :return: 整理好的DataFrame
    """
    import re
    columnss = ['序号', '赔率公司', '终及时盘口', '终胜赔', '终盘让球', '终负赔', '页数', '终变化时间', '初及时盘口',
                '初胜赔', '初盘让球', '初负赔', '初变化时间', '主客同']
    df = pd.DataFrame(ls, columns=columnss)
    ref = re.compile(r"\d+\.\d+")
    df['终胜赔'] = df['终胜赔'].str.extract(r"(\d+\.\d+)")
    df['终负赔'] = df['终负赔'].str.extract(r"(\d+\.\d+)")
    df['终盘让球'] = df['终盘让球'].str.split(' ').str[0]
    df['初盘让球'] = df['初盘让球'].str.split(' ').str[0]
    df = df.drop(columns=['终及时盘口', '初及时盘口', '页数', '终变化时间', '初变化时间', '主客同'])
    return df


def oupei_handle(ls):
    """
    :param ls: 输入亚赔的list
    :return: 整理好的DataFrame
    """
    columns_ou = ['序号', '2', '3', '初胜赔', '初平赔', '初负赔', '终胜赔', '终平赔', '终负赔', '9', '初胜概率',
                  '初平概率',
                  '初负概率', '终胜概率', '终平概率', '终负概率', '16', '初返还率', '终返还率', '19', '初胜凯利',
                  '初平凯利', '初负凯利',
                  '终胜凯利', '终平凯利', '终负凯利', '26']
    df_ou = pd.DataFrame(ls, columns=columns_ou)
    df_ou = df_ou.drop(columns=['3', '9', '16', '19', '26'])
    return df_ou


def get_table(page, strs):
    """
    :param lists: 选择器字符串，可以是xpath，css等格式,'//*[@id="dz"]//table/tbody/tr'
    :return: 一个表格矩阵
    """

    lists = page.query_selector_all(strs)
    li_obj_list = []
    for ls in lists[:2]:
        cells = ls.query_selector_all('td')
        ls_temp = []
        for val in cells:
            ls_temp.append(val.inner_text())
        li_obj_list.append(ls_temp)
    return li_obj_list


def get_table_析(page, strs):
    """
    :param lists: 选择器字符串，可以是xpath，css等格式,'//*[@id="dz"]//table/tbody/tr'
    :return: 一个表格矩阵
    """
    import re
    list_析1 = page.query_selector_all('//h*[@id="zhanji_01"]/div[3]/div/p')
    zhanji_zhu = [ls.inner_text() for ls in list_析1]

    pattern = re.compile(r'\d+')
    matches_析1 = pattern.findall(zhanji_zhu[0])[-5:]

    list_析2 = page.query_selector_all('//*[@id="zhanji_00"]/div[3]/div/p')
    zhanji_ke = [ls.inner_text() for ls in list_析2]
    matches_析2 = pattern.findall(zhanji_ke[0])[-5:]

    list_析3 = page.query_selector_all('//*[@id="zhanji_11"]/div[3]/div/p')
    zhu_zhuchang = [ls.inner_text() for ls in list_析3]
    matches_析3 = pattern.findall(zhu_zhuchang[0])[-5:]

    list_析4 = page.query_selector_all('//*[@id="zhanji_20"]/div[3]/div/p')
    ke_kechang = [ls.inner_text() for ls in list_析4]
    matches_析4 = pattern.findall(ke_kechang[0])[-5:]
    # matches_析1.extend([matches_析2,matches_析3,matches_析4])
    xx1 = matches_析1 + matches_析2
    xx2 = matches_析3 + matches_析4
    return xx1, xx2


####必发分析
def get_table_必发(page, strs):
    lists = page.query_selector_all(strs)
    li_obj_list = []
    for ls in lists[2:5]:
        cells = ls.query_selector_all('td')
        ls_temp = []
        for val in cells[:]:
            ls_temp.append(val.inner_text())
            # print(f'val.inner_text()=={val.inner_text()}')
        li_obj_list.append(ls_temp)
    # print(f'li_obj_list=={li_obj_list}')
    return li_obj_list

def run_dq(playwright: Playwright, st):  # -> None:
    browser = playwright.chromium.launch(headless=True)
    # browser = playwright.firefox.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # 添加这段代码来修改 navigator.webdriver 属性
    page = context.new_page()

    page.goto("https://zx.500.com/zc/")

    page.wait_for_timeout(250)
    page.locator("#duizhen_sel").select_option(st)
    page.wait_for_timeout(350)
    zhudui_names = [td.inner_text().replace('\xa0', '') for td in
                    page.query_selector_all('//*[@id="duizhen_tb"]/tr/td[4]/a[1]')]
    kedui_names = [td.inner_text().replace('\xa0', '') for td in
                   page.query_selector_all('//*[@id="duizhen_tb"]/tr/td[4]/a[2]')]

    shaishi = [item.inner_text() for item in page.query_selector_all('//*[@id="duizhen_tb"]//tr//td[2]')]
    url_order = [item.inner_text() for item in page.query_selector_all('//*[@id="duizhen_tb"]//tr//td[1]')]
    # Convert to datetime format with year as 2024
    date_format = "%m-%d %H:%M"
    game_date = [datetime.strptime(f"2024-{item.inner_text()}", "%Y-%m-%d %H:%M").strftime("%Y/%m/%d") for item in
                 page.query_selector_all('//*[@id="duizhen_tb"]//tr//td[3]')]

    xpath_result = page.inner_text('xpath=//*[@id="duizhen_tb"]/tr[1]/td[4]/i[2]')

    # 新的提取比分的方法￥￥￥￥￥￥￥，20240514
    # 获得历史的td[4]的所有数据，对应的网址：https://zx.500.com/zc/lsdz.php
    # td4_all = np.array([td.inner_text() for td in page.query_selector_all('//*[@id="dz"]//tr/td[4]/*')]).reshape(14, 5)
    # 获得当前和未来的td[4]的所有数据，对应的网址：https://zx.500.com/zc
    td4_all = np.array(
        [td.inner_text() for td in page.query_selector_all('//*[@id="duizhen_tb"]//tr/td[4]/*')]).reshape(14, 5)

    scored_all = [item.inner_text() for item in page.query_selector_all('//*[@id="duizhen_tb"]//tr//td[4]/span[1]')]

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

    ############################
    html_xi = [item.get_attribute('href') for item in page.query_selector_all('//*[@id="duizhen_tb"]/tr/td[5]/a[1]')]
    print('html_xi_dq:', html_xi)
    # html_ya = [item.get_attribute('href')for item in page.query_selector_all('//*[@id="dz"]//tr/td[5]/a[2]')]
    # html_ou = [item.get_attribute('href') for item in page.query_selector_all('//*[@id="dz"]//tr/td[5]/a[3]')]

    # 正则表达式，用于匹配 URL 中的最后一个数字序列
    # pattern = re.compile(r'\d+(?=\.\w+$)')
    pattern = re.compile(r'shuju-(.*)\.shtml')
    extracted_parts = [pattern.search(url).group(1) for url in html_xi]


    # 提取每个 URL 中的数字并打印
    haoma = []
    for url in html_xi:
        match = pattern.search(url)
        if match:
            print(match.group())
            haoma.append(match.group())

    htmls_数据 = [('http://odds.500.com' + '/fenxi/shuju-' + i + '.shtml') for i in extracted_parts]
    htmls_投注 = [('http://odds.500.com' + '/fenxi/touzhu-' + i + '.shtml') for i in extracted_parts]
    htmls_欧赔 = [('http://odds.500.com' + '/fenxi/ouzhi-' + i + '.shtml') for i in extracted_parts]
    htmls_亚赔 = [('http://odds.500.com' + '/fenxi/yazhi-' + i + '.shtml') for i in extracted_parts]
    # htmls_数据 = [('http://odds.500.com' + '/fenxi/shuju-' + i + '.shtml') for i in haoma]
    # htmls_投注 = [('http://odds.500.com' + '/fenxi/touzhu-' + i + '.shtml') for i in haoma]
    # htmls_欧赔 = [('http://odds.500.com' + '/fenxi/ouzhi-' + i + '.shtml') for i in haoma]
    # htmls_亚赔 = [('http://odds.500.com' + '/fenxi/yazhi-' + i + '.shtml') for i in haoma]

    htmls_total = pd.DataFrame(
        {"shaishi": shaishi, "game_date": game_date, "url_order": url_order, "zhudui_paiming": zhudui_paiming,
         "zhudui_name": zhudui_names,
         "zhudui_scored_all": zhudui_scored_all, "kedui_scored_all": kedui_scored_all, "kedui_name": kedui_names,
         "kedui_paiming": kedui_paiming,
         "ouzhi_urls": htmls_欧赔, "yazhi_urls": htmls_亚赔, "shuju_urls": htmls_数据, "touzhu_urls": htmls_投注})
    context.close()
    browser.close()
    return htmls_total

def run_lsdz(playwright: Playwright, st):  # -> None:
    browser = playwright.firefox.launch(headless=True)
    # browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # 添加这段代码来修改 navigator.webdriver 属性
    page = context.new_page()
    # page.goto("https://zx.500.com/zc/")
    page.goto("https://zx.500.com/zc/lsdz.php")
    page.wait_for_timeout(random.randint(100, 300))
    page.get_by_role("combobox").select_option(st)

    ########################################################################
    # 定义数值范围和对应的概率
    ranges = [(50, 100), (101, 200), (201, 500)]
    probabilities = [0.6, 0.3, 0.1]  # 概率总和应为 1，这里需要调整以确保总和为 1

    # 标准化概率，使其总和为 1
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()

    # 根据概率选择一个范围
    selected_range = np.random.choice(len(ranges), p=probabilities)

    # 在选定的范围内生成一个随机数
    random_number = np.random.randint(ranges[selected_range][0], ranges[selected_range][1] + 1)

    #############################################################################

    # page.wait_for_timeout(random.randint(150, 300))
    page.wait_for_timeout(random_number)

    zhudui_names = [td.inner_text().replace('\xa0', '') for td in
                    page.query_selector_all('//*[@id="dz"]//tr/td[4]/span[2]')]
    kedui_names = [td.inner_text().replace('\xa0', '') for td in
                   page.query_selector_all('//*[@id="dz"]//tr/td[4]/span[4]')]

    shaishi = [item.inner_text() for item in page.query_selector_all('//*[@id="dz"]//tr//td[2]')]
    changchi = [item.inner_text() for item in page.query_selector_all('//*[@id="dz"]//tr//td[1]')]
    # Convert to datetime format with year as 2024
    date_format = "%m-%d %H:%M"
    game_date = [datetime.strptime(f"2024-{item.inner_text()}", "%Y-%m-%d %H:%M").strftime("%Y/%m/%d") for item in
                 page.query_selector_all('//*[@id="dz"]//tr//td[3]')]

    # xpath_result = page.query_selector_all('xpath=//*[@id="dz"]/tr[1]/td[4]')

    ################################&&&&&&&&&&&&&&&&&&&&&&&&&&77777777777777777777777777777777
    td4_all = np.array([td.inner_text() for td in page.query_selector_all('//*[@id="dz"]//tr/td[4]/*')]).reshape(14, 5)
    zhudui_scored_all = []
    kedui_scored_all = []
    zhudui_paiming = []
    kedui_paiming = []
    zhudui_names = []
    kedui_names = []
    # for item in scored_all:
    for item in td4_all:
        # print(f"item[0]={item[0]}, item[1]={item[1]},item[2]={item[2]},item[3]={item[3]},item[4]={item[4]}")
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
    ###########################&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7777777777777777777777777777777777

    html_xi = [item.get_attribute('href') for item in page.query_selector_all('//*[@id="dz"]//tr/td[5]/a[1]')]
    # html_ya = [item.get_attribute('href')for item in page.query_selector_all('//*[@id="dz"]//tr/td[5]/a[2]')]
    # html_ou = [item.get_attribute('href') for item in page.query_selector_all('//*[@id="dz"]//tr/td[5]/a[3]')]
    print('html_xi_ls:',html_xi)
    # 正则表达式，用于匹配 URL 中的最后一个数字序列
    # pattern = re.compile(r'\d+(?=\.\w+$)')
    pattern = re.compile(r'shuju-(.*)\.shtml')
    extracted_parts = [pattern.search(url).group(1) for url in html_xi]

    # 提取每个 URL 中的数字并打印
    haoma = []
    for url in html_xi:
        match = pattern.search(url)
        if match:
            print(match.group())
            haoma.append(match.group())

    # htmls_数据 = [('http://odds.500.com' + '/fenxi/shuju-' + i + '.shtml') for i in haoma]
    # htmls_投注 = [('http://odds.500.com' + '/fenxi/touzhu-' + i + '.shtml') for i in haoma]
    # htmls_欧赔 = [('http://odds.500.com' + '/fenxi/ouzhi-' + i + '.shtml') for i in haoma]
    # htmls_亚赔 = [('http://odds.500.com' + '/fenxi/yazhi-' + i + '.shtml') for i in haoma]
    htmls_数据 = [('http://odds.500.com' + '/fenxi/shuju-' + i+ '.shtml' ) for i in extracted_parts]
    htmls_投注 = [('http://odds.500.com' + '/fenxi/touzhu-' + i + '.shtml') for i in extracted_parts]
    htmls_欧赔 = [('http://odds.500.com' + '/fenxi/ouzhi-' + i + '.shtml') for i in extracted_parts]
    htmls_亚赔 = [('http://odds.500.com' + '/fenxi/yazhi-' + i + '.shtml') for i in extracted_parts]

    context.close()
    browser.close()
    htmls_total = pd.DataFrame(
        {"shaishi": shaishi, "game_date": game_date, "changchi": changchi, "zhudui_paiming": zhudui_paiming,
         "zhudui_name": zhudui_names,
         "zhudui_scored": zhudui_scored_all, "kedui_scored": kedui_scored_all, "kedui_name": kedui_names,
         "kedui_paiming": kedui_paiming,
         "ouzhi_urls": htmls_欧赔, "yazhi_urls": htmls_亚赔, "shuju_urls": htmls_数据, "touzhu_urls": htmls_投注})
    return htmls_total


with sync_playwright() as playwright:
    js = """
    Object.defineProperties(navigator, {
        webdriver: { get: () => undefined }
    });
    """
    # browser = playwright.firefox.launch(headless=False)
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    page = context.new_page()

    # page.locator("#duizhen_sel").select_option(st)
    # 获得当前和未来所有期号，对应的网址：https://zx.500.com/zc/lsdz.php
    page.goto("https://zx.500.com/zc/")
    # page.locator("#duizhen_sel").select_option(st)
    page.wait_for_timeout(350)
    original_list = [td.inner_text().split() for td in page.query_selector_all('//*[@id="duizhen_sel"]/option')]
    qihao_dq_temp = [num[0][:20] for num in original_list]
    pattern_dq = re.compile(r'\d+')

    # Extract the numeric parts and convert them to integers
    qihao_dq = [(pattern_dq.search(period).group()) for period in qihao_dq_temp]
    # qihao_dq = [num for num in
    #             [td.inner_text().split() for td in page.query_selector_all('//*[@id="duizhen_sel"]/option')][0][
    #                 0].split('\n')]

    # 获得历史对阵所有期号，对应的网址：https://zx.500.com/zc/lsdz.php
    page.goto("https://zx.500.com/zc/lsdz.php")
    page.wait_for_timeout(250)
    # page.get_by_role("combobox").select_option(st)
    # page.wait_for_timeout(350)
    qihao_lsdz_original = [td.inner_text().split("\n") for td in
                           page.query_selector_all('//*[@id="dz"]/div[1]/div/span/select')]
    # Regular expression pattern to match the numeric part
    pattern_ls = re.compile(r'\d+')

    # Extract the numeric parts and convert them to integers
    qihao_dq_lsdz = [(pattern_ls.search(period).group()) for period in qihao_lsdz_original[0]]
    # qihao_dq_lsdz = [num for num in qihao_lsdz_original[0]]
    qihao_dq_only = list(set(qihao_dq) - set(qihao_dq_lsdz))

    # df= pd.read_csv(
    #     r'C:\Users\administrator\20231028\爬取500万网站\scrapy_500\scrapy_get_500\scrapy_get_500\df_all_final.csv',dtype={'qihao': str})
    # qishu_当前 =df.qihao.unique()[::-1]
    # 补充前导0，变为5位长度的字符串 ！！！！
    # qishu_当前 = [num.zfill(5) for num in qishu_当前]
    # qishu_当前=[str(i) for i in range(24077,24065,-1)]
    qishu_当前 = qihao_dq_lsdz[:30]
    htmls_数据_all_lsdz = pd.DataFrame()
    htmls_数据_all_dq = pd.DataFrame()

    for st in qishu_当前[:]:
        print(f'st=={st}')
        js = """
        Object.defineProperties(navigator, {
            webdriver: { get: () => undefined }
        });
        """
        # time_jiange = random.randint(100, 300)
        # -------------------20240513------------------------
        # browser = playwright.firefox.launch(headless=False)
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        page.goto("https://zx.500.com/zc/lsdz.php")
        page.wait_for_timeout(250)
        page.get_by_role("combobox").select_option(st)
        page.wait_for_timeout(350)
        htmls_all_return_lsdz = run_lsdz(playwright, st)
        # htmls_all_return_dq = run_dq(playwright, st)
        htmls_all_return_lsdz['qihao'] = st
        htmls_数据_all_lsdz = pd.concat([htmls_数据_all_lsdz, htmls_all_return_lsdz])
    htmls_数据_all_lsdz.to_excel('htmls_数据_all_lsdz.xlsx')
    print('save htmls_数据_all_lsdz.xlsx finished!!!')

    for st in qihao_dq_only[:]:
        print(f'st=={st}')
        js = """
        Object.defineProperties(navigator, {
            webdriver: { get: () => undefined }
        });
        """
        # time_jiange = random.randint(100, 300)
        # -------------------20240513------------------------
        # browser = playwright.firefox.launch(headless=True)
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        # page.goto("https://zx.500.com/zc/lsdz.php")
        page.goto("https://zx.500.com/zc/")
        page.wait_for_timeout(250)
        page.locator("#duizhen_sel").select_option(st)
        # page.get_by_role("combobox").select_option(st)
        page.wait_for_timeout(350)
        # htmls_all_return_lsdz=run_lsdz(playwright,st)
        htmls_all_return_dq = run_dq(playwright, st)
        htmls_all_return_dq['qihao'] = st
        htmls_数据_all_dq = pd.concat([htmls_数据_all_dq, htmls_all_return_dq])
    htmls_数据_all_dq.to_excel('htmls_数据_all_dq.xlsx')

    print('save htmls_数据_all_dq.xlsx finished!!!')


