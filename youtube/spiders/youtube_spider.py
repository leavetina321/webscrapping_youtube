from scrapy import Spider 
from youtube.items import YoutubeItem
from scrapy import Request
import re 


class youtubeSpider(Spider):
    name = 'youtube_spider'
    allowed_urls = ['https://socialblade.com/']
    start_urls = ['https://socialblade.com/youtube/top/category/auto']

    def parse(self, response):
        links=response.xpath('//div[@style="width: 340px; background: #f6f6f6; padding: 0px 0px; color:#90CAF9; text-transform: uppercase; font-size: 8pt;"]//a/@href').extract()[4:]

        for link in links:
            yield Request(url= 'http://socialblade.com{}'.format(link), callback=self.parse_detail_page)


    def parse_detail_page(self, response):
        page_link=response.xpath('//div[@style="float: right; width: 900px;"]//div[@style="float: left; width: 350px; line-height: 25px;"]/a/@href').extract()
        for link in page_link:
            yield Request(url= 'http://socialblade.com{}'.format(link), callback=self.parse_user_page)

    def parse_user_page(self, response):
        item = YoutubeItem()
        item['youtuber'] = response.xpath('//h1[@style="float: left; font-size: 1.4em; font-weight: bold; color:#333; margin: 0px; padding: 0px; margin-right: 5px;"]/text()').extract_first() 
        number_list=response.xpath('//span[@style="font-weight: bold;"]/text()').extract()
        string_list=response.xpath('//span[@style="font-weight: bold;"]/a/text()').extract()
        price_list=list(map(str.strip, response.xpath('//p[@style="font-size: 1.4em; color:#41a200; font-weight: 600; padding-top: 20px;"]/text()').extract()))
        item['uploads']=int(number_list[0].replace(",",''))
        item['subs']=int(number_list[1].replace(",",''))
        item['video_view']=int(number_list[2].replace(",",''))
        item['date']=number_list[3]
        if len(string_list[0])==2:
            item['country']=string_list[0]
        else:
            item['country']=None

        try:
            item['channel_type']=string_list[1]
        except:
            item['channel_type']=string_list[0]

        item['e_m_earnings']=price_list[0]
        item['e_y_earnings']=price_list[1]
        item['view_last30']=int(response.xpath('//span [@id="afd-header-views-30d"]/text()').extract_first().strip().replace(",",''))
        item['sub_last30']=int(response.xpath('//span [@id="afd-header-subs-30d"]/text()').extract_first().strip().replace(",",''))
        item['grade']=response.xpath('//p[@style="font-size: 2.8em; font-weight: 600;"]/span/text()').extract_first()

        sign1=response.xpath('//span[@id="afd-header-views-30d-perc"]//i[@class="fa fa-caret-down"]').extract()

        if len(sign1)==0:
            change1=response.xpath('//span[@id="afd-header-views-30d-perc"]//span[@style]/text()').extract()[0]
            item['view_change']=int(re.findall('\d+',change1)[0])   
        else:
            change2= response.xpath('//span[@id="afd-header-views-30d-perc"]//span[@style]/text()').extract()[0]
            item['view_change']= -(int(re.findall('\d+',change2)[0]))
       
        sign2=response.xpath('//span[@id="afd-header-subs-30d-perc"]//i[@class="fa fa-caret-down"]').extract()
        if len(sign2)==0:
            try:
                change3=response.xpath('//span[@id="afd-header-subs-30d-perc"]//span[@style]/text()').extract()[0]
                item['sub_change']=int(re.findall('\d+',change3)[0])
            except:
                item['sub_change']=None
              
        else:
            change4=response.xpath('//span[@id="afd-header-subs-30d-perc"]//span[@style]/text()').extract()[0]
            item['sub_change']= -(int(re.findall('\d+',change4)[0]))


        yield item