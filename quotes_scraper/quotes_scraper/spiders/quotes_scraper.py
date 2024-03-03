import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self):
        super().__init__()
        self.quotes = []
        self.authors = {}

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_data = {
                'quote': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            self.quotes.append(quote_data)

            author_name = quote_data['author']
            if author_name not in self.authors:
                author_link = quote.css('span a::attr(href)').get()
                yield response.follow(author_link, self.parse_author, meta={'author_name': author_name})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            self.save_to_json()

    def parse_author(self, response):
        author_name = response.request.meta['author_name']
        born_date = response.css('span.author-born-date::text').get()
        description = response.css('div.author-description::text').get()

        self.authors[author_name] = {
            'fullname': author_name,
            'born_date': born_date.strip() if born_date else None,
            'description': description.strip() if description else None
        }

    def save_to_json(self):
        with open('quotes.json', 'w') as f:
            json.dump(self.quotes, f, indent=2)

        with open('authors.json', 'w') as f:
            json.dump(list(self.authors.values()), f, indent=2)
