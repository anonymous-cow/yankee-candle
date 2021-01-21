
import scrapy



class YankeecandleSpider(scrapy.Spider):
	user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

	name = 'yankeeCandle'
	allowed_domains = ['www.amazon.com']
	start_urls = ['https://www.amazon.com/Yankee-Candle-Large-Balsam-Cedar/product-reviews/B000JDGC78/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews/']
	custom_settings={'FEED_URI':'amazon-candle.csv','FEED_FORMAT':'csv'}

	def parse(self, response):
		for review in response.xpath('//div[@data-hook="review"]'):
			yield{
				
				'name':review.xpath(".//div[@class='a-profile-content']//text()").get(),
				'info':review.xpath(".//a[@data-hook='format-strip']/text()").getall(),
				'rating':review.xpath(".//i[@data-hook='review-star-rating']//text()").get(),
				'title':review.xpath(".//a[@data-hook='review-title']/span/text()").get(),
				'text':review.xpath(".//span[@data-hook='review-body']/span//text()").getall(),
				'date':review.xpath(".//span[@data-hook='review-date']/text()").get(),
				'url':response.url
			}


		next_page = response.css('.a-last a::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)

