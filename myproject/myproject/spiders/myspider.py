import scrapy
import logging


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["ibolak.com"]
    start_urls = ["https://ibolak.com/shop/categories/nb1kd/cover"]

    def parse(self, response):
        product_links = response.css('div.col-lg-3.col-sm-12 a.product-wrapper::attr(href)').getall()
        for product_link in product_links:
            yield response.follow(product_link, self.parse_product)

    def parse_product(self, response):

        logging.info(f"Scraping product page: {response.url}")

        product_name = response.css('h1::text').get()
        product_price = response.css('div#product-price strong::text').get()

        if product_name:
            product_name = product_name.strip()
            logging.info(f"Product name extracted: {product_name}")
            if product_price:
                product_price = product_price.strip().replace('تومان', '').replace(',', '').strip()
                logging.info(f"Product price extracted: {product_price}")
                yield {
                    'name': product_name,
                    'price': product_price
                }
        else:
            logging.error(f"Failed to extract product name from: {response.url}")
