import scrapy

from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'stack'
    allowed_domains = ['dakarmatin.com']
    start_urls = ['https://www.dakarmatin.com/']

    def parse(self, response):
        for quote in response.css('div.jeg_posts_wrap > div > article.jeg_post.jeg_pl_md_box'):
            item = QuoteItem()

            for element in quote.css("h3.jeg_post_title a"):
                item['url'] = element.xpath('@href').extract()[0]
            item['category'] = quote.css('div.jeg_post_category  a::text').get()
            item['date'] = quote.css('div.jeg_meta_date a::text').get()
            item['tags'] = quote.css('h3.jeg_post_title a::text').get()
            for element in quote.css("div.thumbnail-container img"):
                item['image'] = element.xpath('@data-src').extract()[0]

            yield item

        # Find the "Voir plus ->" button and follow the link
        for a in response.css('div.jeg_block_loadmore a'):
            yield response.follow(a, callback=self.parse)