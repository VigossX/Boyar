# -*- coding:utf-8 -*-
import scrapy
import cx_Oracle
import uuid


class boyar136(scrapy.Spider):
    name = "boyar136"
    dic = {}
    url = 'http://www.boyar.cn/column/136/'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse_1(self, response, title, date):
        td_lst = []
        cur_arr = []
        trs = response.css('div#ctn tr[height="17"]')
        for tr in trs:
            cur_arr = tr.css('td *::text').extract()
            num = len(cur_arr)
            if num == 7:
                cur_arr.insert(0, td_lst[len(td_lst) - 1][0])
            elif cur_arr[0] == '合计':
                break
            td_lst.append(cur_arr)
        # 连接oracle
        # try:
        #     conn = cx_Oracle.connect(
        #         'tmis_test2018/tmis_test2018@47.100.1.178/tmis')
        #     curs = conn.cursor()
        #     i = 0
        #     for row in td_lst:
        #         # sql语句
        #         sqlUpd = 'INSERT INTO BOYAR_135 ("DATA_ID","PROVINCE","CITY","DATA_1","DATA_2","DATA_3","DATA_4","DATA_5","DATA_6","TITLE","OPEN_DATE") VALUES (\'' + str(uuid.uuid1(
        #         ))+'\',\'' + row[0] + '\',\'' + row[1] + '\',\'' + row[2] + '\',\'' + row[3] + '\',\'' + row[4] + '\',\'' + row[5] + '\',\'' + row[6] + '\',\'' + row[7] + '\',\'' + title + '\',TO_DATE(\'' + date + '\', \'YYYY-MM-DD\'))'
        #         curs.execute(sqlUpd)
        #         i = i + 1
        #         if i == 100:
        #             conn.commit()
        #             i = 0
        # finally:
        #     conn.commit()
        #     curs.close()
        #     conn.close()

    def parse(self, response):
        cur_page = response.css('div#feed_lb')
        for per in cur_page:
            # url连接
            key = per.css('a::attr(href)').extract_first()
            # 文字题目，日期
            lst = [per.css('a::text').extract_first(), per.css(
                'div.lmrq::text').extract_first()]
            value = lst
            self.dic[key] = value

        next_page_flag = response.css('a::attr(title)').extract()
        if '下一页' in next_page_flag:
            # 访问下一页
            next_str = response.css(
                'a[title="下一页"]::attr(href)').extract_first()
            next_page = next_str[next_str.index('(') + 1:-1]
            headers = {
                "HOST": "www.boyar.cn",
                "Referer": "http://www.boyar.cn/column/136/",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
            }
            post_url = self.url
            post_data = {
                "column_id": str(67),
                "page": next_page
            }
            yield scrapy.FormRequest(url=post_url, method='POST', headers=headers, formdata=post_data, dont_filter=True, callback=self.parse)
        else:
            # pass
            filename = 'boyar136.txt'
            print(len(self.dic))
            with open(filename, 'a') as f:
                for key, value in self.dic.items():
                    f.write('%s\t: %s\n' % (key, value))

                self.log('保存文件: %s' % filename)
            # i = 0
            # for key, value in self.dic.items():
            #     yield scrapy.Request(url=key, callback=lambda response, title=value[0], date=value[1]: self.parse_1(response, title, date))
                # i += 1
                # if i == 2:
                #     return
