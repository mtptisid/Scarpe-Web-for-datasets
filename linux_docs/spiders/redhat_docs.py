import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Precompiled regex patterns for cleaning unwanted content
PATTERNS = {
    'legal': re.compile(r'(?:Legal Notice|Copyright.*?Red Hat|All rights reserved|Terms of Use).*?(?=\n\S|\Z)', re.DOTALL | re.I),
    'nav': re.compile(r'\b(?:Table of Contents|Previous\s*\|\s*Next|Previous|Next|Back to top|Format:|Multi-page|Single-page|View full doc as PDF)\b', re.I),
    'metadata': re.compile(r'^\s*(?:Document ID|Version:|Last updated:|Category:)\s.*$', re.M),
    'section': re.compile(r'^(#{1,4} .+?|Chapter \d+:|[A-Z][A-Z\s]+[A-Z])\s*$', re.M),
    'command': re.compile(r'^\s*(?:# |\$ |oc |kubectl |rpm |yum )(.*?)(?=\s*#|$)', re.M),
    'version': re.compile(r'(?:OpenShift|RHEL)\s+(?:Container Platform|Version)?\s*(\d+\.\d+\.\d+|\d+\.\d+)'),
    'yaml_block': re.compile(r'```yaml\n(.*?)```', re.DOTALL),
    'json_block': re.compile(r'```json\n(.*?)```', re.DOTALL),
    'redundant_headers': re.compile(r'^(.*?)(?=\1\s+\d+\.\d+)', re.M)  # Catch duplicate TOC headers
}

class RedHatDocsSpider(CrawlSpider):
    name = "redhat_docs"
    allowed_domains = ["access.redhat.com", "docs.redhat.com"]
    start_urls = ["https://docs.redhat.com/en"]

    custom_settings = {
        'FEED_FORMAT': 'jsonlines',
        'FEED_URI': 'datasets/redhat/docs.jsonl',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'DEBUG',  # Show more details in logs
    }

    rules = (
        Rule(LinkExtractor(allow=r'/en/documentation/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # Extract title
        title = response.css('h1.chapter-title::text').get('').strip()

        # Extract & Clean Content
        content_container = response.css('div.docs-content-container')
        
        # Remove unwanted navigation elements before extracting text
        for nav in content_container.css('a, span, div'):
            if PATTERNS['nav'].search(nav.get()):
                nav.extract()

        # Extract & clean text
        content = self.clean_text(content_container.xpath('.//text()').getall())

        # Extract commands/code from <rh-code-block> and .codeblock__wrapper
        commands = []
        for code_block in response.css('rh-code-block pre, rh-code-block code, .codeblock__wrapper pre'):
            cmd_text = '\n'.join(code_block.css('::text').getall()).strip()
            if cmd_text:
                commands.append(cmd_text)

        # Apply regex filters
        content = self.apply_filters(content)

        # Yield structured data
        yield {
            'title': title,
            'content': content if content else None,
            'commands': commands if commands else None,
            'url': response.url
        }

    def clean_text(self, text_elements):
        """Clean up text by removing extra spaces and newlines."""
        cleaned = ' '.join([text.strip() for text in text_elements if text.strip()])
        return re.sub(r'\s+', ' ', cleaned).strip()

    def apply_filters(self, text):
        """Applies regex filters to remove legal notices, metadata, and unwanted navigation text."""
        if isinstance(text, list):  # If content is a list of text segments, join into a string first
            text = ' '.join(text)

        # Apply filtering
        for pattern in PATTERNS.values():
            text = pattern.sub('', text)

        return text.strip() if text else None