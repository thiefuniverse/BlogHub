#!/bin/python3

from blog_config import Config
# extract links like jQuery
from pyquery import PyQuery as PQ
# a html request with JS render
from requests_html import HTMLSession

class Crawler:
    def GetHtml(self, url):
        "get html by requests-html which can render js."
        session=HTMLSession()
        s = session.get(url)
        # sleep 3 seconds ot wait other files rendered completely without js.
        # then render js script.
        s.html.render(sleep=6,wait=5, keep_page=True)
        return s.html.html

    def GetAllLinks(self, config, results):
        if config.root_url:

            html = self.GetHtml(config.root_url)
        else:
            print("config.root_url is empty. whoopos error!")
            return
        # print(html)
        index_html = PQ(html)
        a_html = index_html(config.css_selector)
        # print(index_html)
        for x in a_html.items():
            href = x.attr('href')
            print("link:", href)
            if href:
                results.add(href)

# test 
if __name__ == "__main__":
    craw = Crawler()
    c = Config()
    c.Load("blog_index_selector/csdn.def.json")

    res = set()
    craw.GetAllLinks(c, res)
    print(len(res))
