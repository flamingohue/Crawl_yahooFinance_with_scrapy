import scrapy
from ..items import StockprojectItem
from stockproject.companies import interested_companies
class MostactiveSpider(scrapy.Spider):
    name = 'activestock'
    def start_requests(self):
        headers = { 'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0;'}
        urls = ['https://finance.yahoo.com/quote/' + company for company in interested_companies]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse, headers=headers)
    
    def parse(self,response):
        items = StockprojectItem()

        items['stock_name'] = response.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').css('::text').extract()
        items['intraday_price'] = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div').css('::text').extract_first()
        items['price_change'] = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').css('::text').extract()
        items['current_timestamp'] = response.xpath('//*[@id="quote-market-notice"]/ span').css('::text').extract()
        items['prev_close'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]').css(
            '::text').extract()
        items['open'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]').css(
            '::text').extract()
        items['bid'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]').css(
            '::text').extract()
        items['ask'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[4]/td[2]').css(
            '::text').extract()
        items['range_day'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').css(
            '::text').extract()
        items['range_52weeks'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]').css(
            '::text').extract()
        items['volume'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]').css(
            '::text').extract()
        items['volume_avg'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]').css(
            '::text').extract()
        items['market_cap'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]').css(
            '::text').extract()
        items['beta_5yr_monthly'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]').css(
            '::text').extract()
        items['pe_ratio'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]').css(
            '::text').extract()
        items['eps'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]').css(
            '::text').extract()
        items['earnings_date'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]/span[1]').css(
            '::text').extract()
        items['fwd_div_yield'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]').css(
            '::text').extract()
        items['exp_div_date'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[7]/td[1]/span').css(
            '::text').extract()
        items['est_yr_target'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[8]/td[2]').css(
            '::text').extract()

        yield items