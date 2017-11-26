from flask import render_template, request
import subprocess

from app import app 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/account', methods=['POST'])
def account():
    account = request.form['account_name']
    setup_scraper(account)
    return 'hello sir, ' + account

def spider_closing(spider):
    """Activates on spider closed signal"""
    reactor.stop()

def setup_scraper(account):
    subprocess.call([
        'scrapy', 
        'crawl', 
        'Spidergram', "-a", "account=" + account
    ])

    # settings = Settings()
    # settings.set('ROBOTSTXT_OBEY', False)

    # process = CrawlerProcess(settings)
    # process.crawl(Spidergram, account=account)
    # process.start()

    # crawler = Crawler(Spidergram, settings)
    # crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    # crawler.configure()
    # crawler.crawl(Spidergram(account))
    # crawler.start()
    # reactor.run()
