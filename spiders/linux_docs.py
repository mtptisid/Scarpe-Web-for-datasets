import scrapy
import os
import re
from slugify import slugify
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LinuxDocsSpider(CrawlSpider):
    name = "linux_docs"
    allowed_domains = ["tldp.org"]
    start_urls = ["https://www.tldp.org/"]

    rules = (
        Rule(LinkExtractor(allow=r'/HOWTO/|/FAQ/|/guides.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log(f"Processing URL: {response.url}")
        
        # Try common selectors for Linux docs
        content = response.css('div#content, main, article')
        if content:
            text_elements = content.css('::text').getall()
            self.log(f"Extracted {len(text_elements)} text elements")
            cleaned_text = self.clean_text(text_elements)
            self.log(f"Cleaned text length: {len(cleaned_text)} characters")
            if cleaned_text:
                os.makedirs("datasets/linux", exist_ok=True)
                filename = f"{slugify(response.url)}.txt"
                filepath = os.path.join("datasets/linux", filename)
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