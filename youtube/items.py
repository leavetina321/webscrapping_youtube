# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    youtuber = scrapy.Field()
    grade = scrapy.Field()
    uploads = scrapy.Field()
    subs = scrapy.Field()
    video_view = scrapy.Field()
    date = scrapy.Field()
    country = scrapy.Field()
    channel_type= scrapy.Field()
    e_m_earnings = scrapy.Field()
    e_y_earnings = scrapy.Field()
    view_change = scrapy.Field()
    sub_change = scrapy.Field()
    view_last30 = scrapy.Field()
    sub_last30 = scrapy.Field()