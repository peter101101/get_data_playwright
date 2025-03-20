from threading import Thread

from DrissionPage import ChromiumPage
from DataRecorder import Recorder
import pandas as pd


def collect(tab, recorder, title):
    """用于采集的方法
    :param tab: ChromiumTab 对象
    :param recorder: Recorder 记录器对象
    :param title: 类别标题
    :return: None
    """
    num = 1  # 当前采集页数
    while True:
        # 遍历所有标题元素
        str_欧 = 'x://*[@id="datatb"]//table/tbody/tr'
        for tds in tab.eles('x://*[@id="datatb"]//table/tbody/tr'):
            # lists = page.eles(strs)
            li_obj_list = []
            for ls in tds.eles('x:/td'):
                recorder.add_data((ls.text))
            # 获取某页所有库名称，记录到记录器

        if num >=3:
            break
        # 如果有下一页，点击翻页
        # btn = tab('@rel=next', timeout=2)
        # if btn:
        #     btn.click(by_js=True)
        #     tab.wait.load_start()
        #     num += 1
        #
        # # 否则，采集完毕
        # else:
        #     break


def main():
    df = pd.read_excel(r'C:\Users\Administrator\20231028\htmls_数据_all_dq.xlsx', parse_dates=['game_date'],
                       date_format='%Y-%m-%d')
    # 新建页面对象
    page = ChromiumPage()
    # 第一个标签页访问网址
    # page.get('https://gitee.com/explore/ai')
    page.get(df.ouzhi_urls[0])
    # 获取第一个标签页对象
    tab1 = page.get_tab()
    # 新建一个标签页并访问另一个网址
    tab2 = page.new_tab(df.ouzhi_urls[1])
    # 获取第二个标签页对象
    tab2 = page.get_tab(tab2)

    tab3 = page.new_tab(df.ouzhi_urls[2])
    # 获取第二个标签页对象
    tab3 = page.get_tab(tab3)

    # 新建记录器对象
    recorder = Recorder('data_test.csv')

    # 多线程同时处理多个页面
    Thread(target=collect, args=(tab1, recorder, 'ou_1')).start()
    Thread(target=collect, args=(tab2, recorder, 'ou_2')).start()
    Thread(target=collect, args=(tab2, recorder, 'ou_3')).start()


if __name__ == '__main__':
    main()