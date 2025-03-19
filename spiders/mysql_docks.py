import scrapy
import os
import re
from slugify import slugify
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySQLDocsSpider(CrawlSpider):
    name = "mysql_docs"
    allowed_domains = ["dev.mysql.com"]
    start_urls = ["https://dev.mysql.com/doc/"]

    rules = (
        Rule(LinkExtractor(allow=r'/doc/refman/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log(f"Processing URL: {response.url}")
        
        # Try common selectors for MySQL docs
        content = response.css('div.section, main, div#content')
        if content:
            text_elements = content.css('::text').getall()
            self.log(f"Extracted {len(text_elements)} text elements")
            cleaned_text = self.clean_text(text_elements)
            self.log(f"Cleaned text length: {len(cleaned_text)} characters")
            if cleaned_text:
                os.makedirs("datasets/mysql", exist_ok=True)
                filename = f"{slugify(response.url)}.txt"
                filepath = os.path.join("datasets/mysql", filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)
                self.log(f"Saved documentation: {filepath}")
            else:
                self.log("Cleaned text is empty, not saving")
        else:
            self.log("No content found on this page")

    def clean_text(self, text_elements):
        self.log(f"Raw text elements sample: {text_elements[:5]}")
        cleaned = ' '.join([text.strip() for text in text_elements if text.strip()])
        return re.sub(r'\s+', ' ', cleaned).strip()