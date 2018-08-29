# -*- coding: utf-8 -*-

# Scrapy settings for chainxy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chainxy'

SPIDER_MODULES = ['chainxy.spiders']
NEWSPIDER_MODULE = 'chainxy.spiders'

DOWNLOAD_DELAY = 0.5

# Feed export
FEED_FORMAT = 'csv' # exports to csv
FEED_EXPORT_FIELDS = ['code', 'balance', 'validation_date'] # which fields should be exported

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chainxy (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
# COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'chainxy.middlewares.ChainxySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'chainxy.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'chainxy.pipelines.ChainxyPipeline': 300,
}

# FEED_EXPORTERS = {
#     'csv': 'chainxy.exporters.HeadlessCsvItemExporter',
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# -----------------------------------------------------------------------------
# ROTATED PROXY SETTINGS (Local File Backend)
# -----------------------------------------------------------------------------
# DOWNLOADER_MIDDLEWARES = ({
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#     'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
# })
# ROTATED_PROXY_ENABLED = True
# PROXY_STORAGE = 'scrapy_rotated_proxy.extensions.file_storage.FileProxyStorage'
# PROXY_FILE_PATH = ''
# HTTP_PROXIES = [
#     'http://198.1.122.29:80',
#     'http://104.131.77.10:80',
#     'http://50.115.106.98:3128',
#     'http://167.99.157.10:3128',
#     'http://138.68.48.131:8080',
#     'http://159.65.162.141:80',
#     'http://209.97.155.251:8080'
# ]

# HTTPS_PROXIES = [
#     'https://38.29.152.9:53281',
#     'https://35.133.161.106:53281',
#     'https://107.151.131.186:8080',
#     'https://159.89.198.238:3128',
#     'https://35.232.254.10:8080',
#     'https://47.35.216.134:53281',
#     'https://173.164.26.117:3128'
# ]
