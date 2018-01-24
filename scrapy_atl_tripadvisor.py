import scrapy

class TripAdvisorSpider(scrapy.Spider):
    name = 'tripadvisor_reviews_atl'

    custom_settings = {
        "DOWNLOAD_DELAY": 0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }
    start_urls = ["https://www.tripadvisor.com/Attractions-g60898-Activities-Atlanta_Georgia.html"]

    #Add start_urls for each page of activities for given city
    for i in range(1,7):
        base = 'https://www.tripadvisor.com/Attractions-g60898-Activities-oa{}-Atlanta_Georgia.html#ATTRACTION_LIST'
        url = base.format(i*30)
        start_urls.append(url)


    def parse(self, response):
        # Extract the links to the individual activities
        static_url = 'https://www.tripadvisor.com'
        count = 0
        for href_link in response.xpath('//div[@class="listing_title "]/a/@href').extract():
            if href_link.find("Reviews-") > 0:
                href = static_url + href_link

                #Calculate number of pages of reviews available for each activity to improve scrapy efficiency
                review_count = int(response.xpath('//div[@class="rs rating"]/span[2]/a/text()').extract()[count].strip().split()[0].replace(",",""))
                review_pages = int(round(review_count, -1)/10)
                count += 1

                #Extract up to 200 reviews per activity
                for i in range(min(20, review_pages)):
                    if i > 0:
                        if href.find("Reviews-") > 0:
                            beg, end = href.split("Reviews-")
                            href = beg + "Reviews-or" + str(i*10) + "-" + end
                        else:
                            break

                    yield scrapy.Request(
                        url=href, callback=self.parse_tripadvisor,
                        meta={'url':href})
                    href = static_url + href_link

    #Extract activity and reviews data for each activity in given city
    def parse_tripadvisor(self,response):
        try:
            title = response.xpath('//h1[@id="HEADING"]/text()').extract()[0].strip()
        except:
            title = None
        try:
            num_reviews = response.xpath('//span[@property="v:count"]/text()').extract()[0].strip()
        except:
            num_reviews = None
        try:
            rating =  response.xpath('//span[@property="ratingValue"]/@content').extract()[0].strip()
        except:
            rating = None
        try:
            suggested_duration = response.xpath('//div[@class="detail_section duration"]/text()').extract()[0].strip()
        except:
            suggested_duration = None
        try:
            image_links = response.xpath('//span[@class="imgWrap "]/img/@data-src').extract()
        except:
            image_links = None
        #Loop through each review on the page to extract review-specific data
        for review in response.xpath('//div[@class="review-container"]'):

            try:
                bubble_rating =  review.xpath('./div/div/div/div[2]/div/div/div/span[1]/@class').extract()[0]
            except:
                bubble_rating = None

            try:
                review_title = review.xpath('./div/div/div/div[2]/div/div/div[2]/a/span/text()').extract()[0]
            except:
                review_title = None

            try:
                review_text = review.xpath('./div/div/div/div[2]/div/div/div[3]/div/p/text()').extract()[0]
            except:
                review_text = None

            try:
                review_date = review.xpath('./div/div/div/div[2]/div/div/div/span[@class = "ratingDate relativeDate"]/@title').extract()[0]
            except:
                review_date = None

            try:
                contributions_count = review.xpath('./div/div/div/div/div/div/div[2]/div/span[@class="ui_icon pencil-paper"]/following-sibling::span[1]/text()').extract()[0]
            except:
                contributions_count = None

            try:
                helpful_count = review.xpath('./div/div/div/div/div/div/div[2]/div/span[@class="ui_icon thumbs-up-fill"]/following-sibling::span/text()').extract()[0]
            except:
                helpful_count = None

            try:
                username = review.xpath('./div/div/div/div/div/div/div/div/span[@class ="expand_inline scrname"]/text()').extract()[0]
            except:
                username = None

            try:
                userid = review.xpath('.//div[@class="member_info"]/div/@id').extract()[0]
            except:
                userid = None

            try:
                location = review.xpath('./div/div/div/div/div/div/div/div/span[@class ="expand_inline userLocation"]/text()').extract()[0]
            except:
                location = None
            try:
                description = response.xpath('//div[@class="prw_rup prw_common_location_description"]//div[@class="text"]/text()').extract()[0].strip()
            except:
                description = None


            yield {
            'activity_name': title,
            'city': "atlanta",
            'reviewer_rating': bubble_rating,
            'review_title': review_title,
            'review_text': review_text,
            'review_date': review_date,
            'contributions_count': contributions_count,
            'helpful_count': helpful_count,
            'username': username,
            'userid': userid,
            'location': location,
            'star_rating': rating,
            'num_reviews': num_reviews,
            'suggested_duration': suggested_duration,
            'description': description,
            'image_links': image_links
            }
