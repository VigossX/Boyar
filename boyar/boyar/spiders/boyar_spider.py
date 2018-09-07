# -*- coding:utf-8 -*-
import scrapy


class boyar(scrapy.Spider):
    name = "boyar"
    dic = {}
    url = 'http://www.boyar.cn/column/135/'
    i = 0

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        cur_page = response.css('div#feed_lb')
        for per in cur_page:
            # url连接
            key = per.css('a::attr(href)').extract_first()
            # 文字题目，日期
            lst = [per.css('a::text').extract_first(), per.css('div.lmrq::text').extract_first()]
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
                "Referer": "http://www.boyar.cn/column/135/",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
            }
            post_url = self.url
            post_data = {
                "column_id": str(67),
                "page": next_page
            }
            yield scrapy.FormRequest(url=post_url, method='POST', headers=headers, formdata=post_data, dont_filter=True, callback=self.parse)
        else:
            filename = 'pig.txt'
            print(len(self.dic))
            with open(filename, 'a') as f:
                for key, value in self.dic.items():
                    f.write('%s\t: %s\n' % (key, value))

                self.log('保存文件: %s' % filename)
