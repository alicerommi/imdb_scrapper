from scrapy import Spider
import scrapy
import os,json
class Top50Spider(Spider):
    
    name = "imdb_top50"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    file_path = "output/top50_movies.json"

    def __init__(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def parse(self, response):
        movies_data = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract_first())
        for movie_item in movies_data.get('itemListElement')[:50]:
            yield scrapy.Request(
                url=movie_item['item'].get('url'),
                callback=self.parse_details
            )

    def parse_details(self, response):
        movie_data = json.loads(response.xpath("//script[@type='application/ld+json']/text()").extract_first())
        yield {
                    "movie_name": movie_data.get('name'),
                    "year_of_release": movie_data.get('datePublished').split("-")[0],
                    "directors": ", ".join([ele.get('name') for ele in movie_data.get('director')]),
                    "stars": ", ".join([ele.get('name') for ele in movie_data.get('actor')]),
        }