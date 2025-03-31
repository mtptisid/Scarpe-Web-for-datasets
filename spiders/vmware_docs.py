import scrapy
import os
import re
from slugify import slugify
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class VMwareDocsSpider(CrawlSpider):
    name = "vmware_docs"
    allowed_domains = ["techdocs.broadcom.com"]
    start_urls = ["https://techdocs.broadcom.com/"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log(f"Processing URL: {response.url}")
        content = response.css('div.content, main, article')
        if content:
            text_elements = content.css('::text').getall()
            cleaned_text = self.clean_text(text_elements)
            if cleaned_text:
                os.makedirs("datasets/vmware", exist_ok=True)
                filename = f"{slugify(response.url)}.txt"
                filepath = os.path.join("datasets/vmware", filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)
                self.log(f"Saved documentation: {filepath}")
            else:
                self.log("Cleaned text is empty, not saving")
        else:
            self.log("No content found on this page")

    def clean_text(self, text_elements):
        cleaned = ' '.join([text.strip() for text in text_elements if text.strip()])
        return re.sub(r'\s+', ' ', cleaned).strip()
