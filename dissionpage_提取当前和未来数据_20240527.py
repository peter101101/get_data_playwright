from DrissionPage import SessionPage
from DrissionPage import ChromiumPage,ChromiumOptions
from DataRecorder import Recorder
from threading import Thread
from DataRecorder import Filler
from DataRecorder.style import CellStyle
import numpy as np
import re
import pandas as pd
import time
import random
#2023/11/25程序调通！！，待优化，如何并行提高提取速度
def yapei_handle(ls):
    """
    :param ls: 输入亚赔的list
    :return: 整理好的DataFrame
    """
    import re
    columnss = ['序号', '赔率公司', '终及时盘口', '终盘主水', '终盘让球', '终盘客水', '页数', '终变化时间', '初及时盘口',
                '初盘主水', '初盘让球', '初盘客水', '初变化时间', '主客同']
    df = pd.DataFrame(ls, columns=columnss)
    ref = re.compile(r"\d+\.\d+")
    df['终盘主水'] = df['终盘主水'].str.extract(r"(\d+\.\d+)")
    df['终盘客水'] = df['终盘客水'].str.extract(r"(\d+\.\d+)")
    df['终盘让球'] = df['终盘让球'].str.split(' ').str[0]
    df['初盘让球'] = df['初盘让球'].str.split(' ').str[0]
    df = df.drop(columns=['序号', '赔率公司','赔率公司','终及时盘口', '初及时盘口', '页数', '终变化时间', '初变化时间', '主客同'])
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

def get_table_duizhen(page, strs):
    """
    :param lists: 选择器字符串，可以是xpath，css等格式,'//*[@id="dz"]//table/tbody/tr'
    :return: 一个表格矩阵
    '//*[@id="odds_nav_cz"]/li[2]/div/div[2]/table/tbody'
    """
    lists = page.eles(strs)
    li_obj_list = []
    for ls in lists[:]:
        lists = page.eles(strs)
        li_obj_list = []
        for ls in lists[:]:
            cells = ls.eles('td')
            ls_temp = []
            for val in cells:
                ls_temp.append(val.inner_text())
            li_obj_list.append(ls_temp)
    return li_obj_list

def get_table(page, strs):
    """
    :param lists: 选择器字符串，可以是xpath，css等格式,'//*[@id="dz"]//table/tbody/tr'
    :return: 一个表格矩阵
    """
    lists = page.eles(strs)
    li_obj_list = []
    for ls in lists[1:2]:
        cells = ls.eles('td')
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
    # list_析 = page.select_option('//*[@id="zhanji_01"]/div[3]/div/p')
    list_析1 = page.eles('x://*[@id="zhanji_01"]/div[3]/div/p')
    zhanji_zhu = [ls.text for ls in list_析1]

    pattern = re.compile(r'\d+')
    matches_析1 = pattern.findall(zhanji_zhu[0])[1:]

    list_析2 = page.eles('x://*[@id="zhanji_00"]/div[3]/div/p')
    zhanji_ke = [ls.text for ls in list_析2]
    matches_析2 = pattern.findall(zhanji_ke[0])[1:]

    list_析3 = page.eles('x://*[@id="zhanji_11"]/div[3]/div/p')
    zhu_zhuchang = [ls.text for ls in list_析3]
    matches_析3 = pattern.findall(zhu_zhuchang[0])[1:]

    list_析4 = page.eles('x://*[@id="zhanji_20"]/div[3]/div/p')
    ke_kechang = [ls.text for ls in list_析4]
    matches_析4 = pattern.findall(ke_kechang[0])[1:]
    # matches_析1.extend([matches_析2,matches_析3,matches_析4])
    xx1=matches_析1 + matches_析2
    xx2=matches_析3 + matches_析4
    return xx1, xx2

####必发分析
def get_table_必发(page,strs):
    selectors_必发1 = 'x://div[8]/div[1]/table/tbody/tr'
    selectors_必发2 = 'x://div[7]/div[1]/table/tbody/tr'
    if page.eles(selectors_必发1):
        strs = selectors_必发1
    else:
        strs = selectors_必发2

    lists = page.eles(strs)
    li_obj_list = []
    for ls in lists[2:5]:
        cells = ls.eles('x:/td')
        ls_temp = []
        for val in cells[:]:
            ls_temp.append(val.text)
            # print(f'val.text=={val.text}')
        li_obj_list.append(ls_temp)

    return li_obj_list

################################处理%比数据函数#######################################
def data_handle_percent(ls_all_td):
    filt_data = []
    for item in ls_all_td:
        if any(char.isdigit() or char == '.' for char in item):
            if '%' in item:
                filt_data.append(round(float(item.replace('%', '')) / 100, 2))
            else:
                filt_data.append(float(item))
    return filt_data

# def convert_to_float(x):
#     if isinstance(x, str) and '%' in x:
#         return float(x.replace('%', '')) / 100
#     else:
#         return float(x)

def convert_to_float(x):
    try:
        if isinstance(x, str):
            if '%' in x:
                return float(x.replace('%', '')) / 100
            else:
                return float(x)
        elif isinstance(x, (int, float)):
            return float(x)
    except ValueError:
        return x  # 如果转换失败，返回原始值
    except TypeError:
        return x  # 如果类型不匹配，也返回原始值

def remove_douhao(x):
    if isinstance(x, str):
        return x.replace(',','')
    return x

# def convert_to_float(x):
#     return float(x.replace('%', ''))/100 if '%' in x else float(x)

def convert_dash_to_float(x):
    if isinstance(x, str):
        # Replace '-' with '0.01'
        x = x.replace('-', '0.01')
        # Replace comma with nothing if it's a thousands separator
        # or with a dot if it's a decimal separator, depending on your data's locale
        # x = x.replace(',', '')  # Use this if comma is a thousands separator
        # x = x.replace(',', '.')  # Use this if comma is a decimal separator
        try:
            return float(x)
        except ValueError:
            print(f"Error converting {x} to float")
            return x  # Return the original value or a default
    else:
        return x

    def remove_douhao(x):
        if isinstance(x, str):
            return x.replace(',', '')
        return x
################################处理%比数据#######################################
###################################-----start run_ou--------#########################    
def run_ou(qihao,url_order,game_date,zhudui_name,kedui_name,zhudui_paiming,kedui_paiming,zhudui_scored_all,kedui_scored_all,url):
    co = ChromiumOptions().headless()
    page = ChromiumPage(co)
    js = """
    Object.defineProperties(navigator, {
        webdriver: { get: () => undefined }
    });
    """
    page.get(url)
    url_lists_欧 = pd.DataFrame()
    # page.wait_for_timeout(random.randint(300, 500))
    electors_亚 = '#datatb > tbody>tr'
    # selectors_欧 = 'x://*[@id="table_cont"]/table/tbody/tr'
    selectors_欧 = 'x://*[@id="datatb"]/tbody/tr'
    ######获取对阵htmls
    strs_duizheng='x://*[@id="odds_nav_cz"]/li[2]/div/div[2]/table/tbody'
    # html_duizhen=get_table_duizhen(page,strs_duizheng)
    # selectors_必发 ='x://div[8]/div[1]/table/tbody/tr'
    # selectors_必发 = 'body > div.odds_content.odds_tz > div:nth-child(1) > table > tbody >tr'
    #处理欧赔
    li_obj_list_欧=get_table(page, selectors_欧)
    # li_obj_list_欧=data_handle_percent(li_obj_list_欧_temp)

    df_欧=pd.DataFrame(li_obj_list_欧)
    df_欧=oupei_handle(li_obj_list_欧)

    df_欧['zhudui_name']=zhudui_name
    df_欧['kedui_name']=kedui_name
    # df_欧['qihao']=qihao
    df_欧['zhudui_paiming']=zhudui_paiming
    df_欧['kedui_paiming']=kedui_paiming

    # df_欧['url_order'] = url_order
    # df_欧['zhudui_scored_all']=zhudui_scored_all
    # df_欧['kedui_scored_all']=kedui_scored_all
    # df_欧['game_date']=game_date
    url_lists_欧=pd.concat([url_lists_欧,df_欧])
    print(f"url_lists_欧={url_lists_欧}")
    page.close()

    return url_lists_欧
###################################-----end run_ou--------#########################    

###################################-----start run_ya--------#########################    
def run_ya(url,qihao):
    co = ChromiumOptions().headless()
    page = ChromiumPage(co)
    js = """
    Object.defineProperties(navigator, {
        webdriver: { get: () => undefined }
    });
    """
    page.get(url)
  
    url_lists_亚 =  pd.DataFrame()
    # page.wait_for_timeout(random.randint(300, 500))

    # 处理亚赔-----------------------------
    selectors_亚 = '#datatb > tbody>tr'
    li_obj_list_亚 = get_table(page, selectors_亚)
    df_亚=pd.DataFrame(li_obj_list_亚)
    df_亚=yapei_handle(li_obj_list_亚)
    # df_亚['qihao']=qihao
    url_lists_亚=pd.concat([url_lists_亚,df_亚])
    page.close()

    return url_lists_亚

###################################-----end run_ya--------#########################  

###################################-----start run_fenxi--------#########################    
# def run_fenxi(playwright: Playwright,url,qihao):
def run_fenxi( url, qihao, url_order, game_date, zhudui_name, kedui_name, zhudui_paiming, kedui_paiming, zhudui_scored_all, kedui_scored_all):
    co = ChromiumOptions().headless()
    page = ChromiumPage(co)
    js = """
    Object.defineProperties(navigator, {
        webdriver: { get: () => undefined }
    });
    """
    page.get(url)
   
    # url_lists_析1= pd.DataFrame()
    # url_lists_析2 = pd.DataFrame()
    data_析1_all= pd.DataFrame()
    data_析2_all= pd.DataFrame()
    # page.wait_for_timeout(random.randint(200, 400))

    # 处理数据分析--------------------------
    selectors_析 = '#datatb > tbody>tr'
    li_obj_list_析1,li_obj_list_析2=get_table_析(page, selectors_析)
    column_析1=['主近10胜','主近10平','主近10负','主队进球','主队失球','客近10胜','客近10平','客近10负','客队进球','客队失球']
    column_析2=['主主近10胜', '主主近10平', '主主近10负', '主队主场进球', '主队主场失球', '客客近10胜', '客客近10平', '客客近10负', '客队客场进球', '客队客场失球' ]
    df_析1=pd.DataFrame([li_obj_list_析1],columns=column_析1)
    # df_析1.columns=column_析1
    # df_析1['qihao']=qihao
    data_析1_all = pd.concat([data_析1_all, df_析1])

    df_析2=pd.DataFrame([li_obj_list_析2],columns=column_析2)
    # df_析2.columns =column_析2
    # df_析2['qihao']=qihao
    data_析2_all = pd.concat([data_析2_all, df_析2])
    data_析2_all['qihao'] = qihao
    data_析2_all['url_order']=url_order
    data_析2_all['shaishi']=shaishi
    data_析2_all['game_time']=game_date
    data_析2_all['zhudui_scored_all']=zhudui_scored_all
    data_析2_all['kedui_scored_all']=kedui_scored_all

    # print(f'url_lists_析=={url_lists_析}')
    page.close()


    return data_析1_all,data_析2_all

###################################-----end run_shuju--------#########################  

###################################-----start run_bf--------#########################    
# def run_bf(playwright: Playwright,url,qihao,url_order,shaishi,game_date):
def run_bf( url, qihao, url_order, shaishi, game_date):
# def run_bf(playwright: Playwright, url, qihao):

    co = ChromiumOptions().headless()
    page = ChromiumPage(co)

    js = """
    Object.defineProperties(navigator, {
        webdriver: { get: () => undefined }
    });
    """
    page.get(url)
    # page.wait_for_timeout(300)
    # page.wait_for_timeout(random.randint(300, 500))
    selectors_亚 = '#datatb > tbody>tr'
    # selectors_欧 = 'x://*[@id="table_cont"]/table/tbody/tr'
    selectors_欧 = '#datatb > tbody>tr'
    ######获取对阵htmls
    strs_duizheng='x://*[@id="odds_nav_cz"]/li[2]/div/div[2]/table/tbody'
    # html_duizhen=get_table_duizhen(page,strs_duizheng)
    selectors_必发 ='x://body/div[@class="odds_content odds_tz"]/div[1]/table/tbody/tr'
    # selectors_必发 = 'body > div.odds_content.odds_tz > div:nth-child(1) > table > tbody >tr'

    ######获取对阵htmls,必发数据------------------------
     ######2024/05/05，必发需要改代码，不要舍去一些信息###########？？？？？？？？？？？？？？？
    # selectors_必发 = 'x://div[8]/div[1]/table/tbody/tr'
    # selectors_必发 = 'x://table/tbody/tr'
    # selectors_必发 = 'body > div.odds_content.odds_tz > div:nth-child(1) > table > tbody >tr'
    # selectors_必发 = '#datatb > tbody'
    li_obj_list_必发 = get_table_必发(page, selectors_必发)
    uuu1 = []
    uuu2 = []
    uuu3 = []

    uuu4 = []
    uuu5 = []
    uuu6 = []
    uuu7=[]
    for i in li_obj_list_必发:
        uuu1.append((i[4]))
        uuu2.append((i[5]))
        uuu3.append((i[6]))
        uuu4.append((i[7]))
        uuu5.append((i[9]))
        uuu6.append((i[10]))
        uuu7.append(i[4:8]+i[9:])
    uuu7=np.array(uuu7)
    uuu7_h=uuu7.reshape(-1,uuu7.shape[1]*3)

    # columns_bf = ['必发胜', '必发平', '必发负', '胜成交价', '平成交价', '负成交价', '胜成交量', '平成交量', '负成交量']
    columns_bf = ['必发胜', '胜成交价','胜成交量','胜庄家盈亏','胜冷热指数','胜盈亏指数',
                  '必发平', '平成交价', '平成交量','平庄家盈亏','平冷热指数','平盈亏指数',
                  '必发负', '负成交价', '负成交量','负庄家盈亏','负冷热指数','负盈亏指数']
    # df_必发 = pd.DataFrame([uuu1 + uuu2 + uuu3+uuu4+uuu5+uuu6], columns=columns_bf)
    # df_必发 = pd.DataFrame([li_obj_list_必发])
    df_必发 = pd.DataFrame(uuu7_h,columns=columns_bf)
    # df_必发['qihao'] = qihao
    # df_必发['url_order']=url_order
    # df_必发['shaishi']=shaishi
    # df_必发['game_time']=game_date

    page.close()

    return df_必发

###################################-----end run_bf--------#########################  
# 自定义日期解析函数，只保留年月日
def custom_date_parser(x):
    return pd.to_datetime(x).date()


start_time = time.time()  # 开始计时
js = """
Object.defineProperties(navigator, {
    webdriver: { get: () => undefined }
});
"""
# df_all = pd.read_excel('htmls_所有数据总和_03028_23148.xlsx')
# df=df_all.head(2800)
# df_all = pd.read_excel('htmls_当前和未来_all.xlsx',parse_dates=['game_date'], date_parser=custom_date_parser)
# df_all = pd.read_excel('htmls_当前和未来_all.xlsx', parse_dates=['game_date'], date_format='%Y-%m-%d')
df_all = pd.read_excel(r'C:\Users\Administrator\20231028\htmls_数据_all_dq.xlsx', parse_dates=['game_date'], date_format='%Y-%m-%d')

# 提取n期，n为14的倍数，n=14*50，代表提取50期，每期14场共14*50组欧赔，亚赔，数据分析，投注分析的数据
# n=50
# df_all['game_date'] = df_all['game_date'].apply(custom_date_parser)
df_all['game_date'] = pd.to_datetime(df_all['game_date'], format='%Y-%m-%d').dt.date
#提取n期，n为14的倍数，n=14*50，代表提取50期，每期14场共14*50组欧赔，亚赔，数据分析，投注分析的数据
# n=50
df = df_all.loc[:]
data_欧_all = pd.DataFrame()
data_亚_all = pd.DataFrame()
data_析1_all=pd.DataFrame()
data_析2_all =  pd.DataFrame()
data_必发_all=pd.DataFrame()

for (qihao,url_order,game_date,shaishi,zhudui_name,kedui_name,zhudui_paiming,kedui_paiming,zhudui_scored_all,kedui_scored_all,ouzhi_urls,yazhi_urls,shuju_urls,touzhu_urls) in zip(df.qihao,df.url_order,df.game_date,df.shaishi,df.zhudui_name,df.kedui_name,
                                                       df.zhudui_paiming,df.kedui_paiming,df.zhudui_scored_all,df.kedui_scored_all,
                                                       df.ouzhi_urls,df.yazhi_urls,df.shuju_urls,df.touzhu_urls):

    # data_析1, data_析2, data_亚, data_欧, data_必发 = run(playwright, st)
    ###获取欧赔并整理数据

    print(f"qihao={qihao}")
    data_欧= run_ou(qihao,url_order,game_date,zhudui_name,kedui_name,zhudui_paiming,kedui_paiming,zhudui_scored_all,kedui_scored_all,ouzhi_urls)
    data_欧_all = pd.concat([data_欧_all, data_欧])


    ###获取亚赔并整理数据
    data_亚= run_ya( yazhi_urls, qihao)
    data_亚_all = pd.concat([data_亚_all, data_亚])
    ###获取数据分析并整理数据----对阵近10场胜负，进失球数
    data_析1,data_析2 = run_fenxi(shuju_urls, qihao, url_order, game_date, zhudui_name, kedui_name, zhudui_paiming, kedui_paiming, zhudui_scored_all, kedui_scored_all)
    data_析1_all = pd.concat([data_析1_all, data_析1])
    data_析2_all = pd.concat([data_析2_all, data_析2])

    ###获取投注分析并整理数据--必发数据
    # data_必发 = run_bf(playwright, touzhu_urls, qihao)
    data_必发 = run_bf(touzhu_urls, qihao, url_order, shaishi, game_date)

    data_必发_all = pd.concat([data_必发_all, data_必发])
    # data_必发_all=data_必发_all.applymap(convert_to_float)
    # print(url_lists_平)
# data_欧_all = data_欧_all.applymap(convert_to_float)
# 应用函数到所有字符串类型的列
for column in data_欧_all.columns:
    if data_欧_all[column].dtype == object:  # 通常字符串列的 dtype 是 object
        # result_ou = data_欧_all[column].map(remove_douhao)
        # data_欧_all[column] = result_ou.map(convert_to_float)
        data_欧_all[column] = data_欧_all[column].apply(convert_to_float)
for column in data_必发_all.columns:
    if data_必发_all[column].dtype == object:  # 通常字符串列的 dtype 是 object
        # data_必发_all[column] = data_必发_all[column].apply(convert_to_float)
        # data_必发_all[column] = data_必发_all[column].apply(convert_dash_to_float)
        result1 = data_必发_all[column].map(remove_douhao)
        result2 = result1.map(convert_to_float)
        result3 = result2.map(convert_dash_to_float)
        # result3 = result2.map(convert_dash_to_float)
        data_必发_all[column] = result3
        # data_必发_all[column] = result3.map(lambda x: pd.to_numeric(x, errors='ignore'))
data_欧_all.reset_index(drop=True, inplace=True)
data_亚_all.reset_index(drop=True, inplace=True)
data_析1_all.reset_index(drop=True, inplace=True)
data_析2_all.reset_index(drop=True, inplace=True)
data_必发_all.reset_index(drop=True, inplace=True)
data_all=pd.concat([data_欧_all,data_亚_all,data_析1_all,data_析2_all,data_必发_all],axis=1)
data_all.to_excel('data_当前_all数据_补.xlsx',
                sheet_name='Sheet1',
                index=False,
                float_format="%.2f")
# data_析1_all.to_excel('data_析1_all.xlsx')
# data_析2_all.to_excel('data_析2_all.xlsx')
# data_亚_all.to_excel('data_亚_all.xlsx')
# data_欧_all.to_excel('data_欧_all.xlsx')
# data_必发_all.to_excel('data_必发_all.xlsx')
print('finished!!!')
end_time = time.time()  # 结束计时
print('Optimization complete and data processed!')
print(f"Total runtime: {end_time - start_time:.2f} seconds")
