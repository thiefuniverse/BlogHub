#!/bin/python3

# extract links like jQuery
from pyquery import PyQuery as PQ
# a html request with JS render
from requests_html import HTMLSession

import urllib.request
def GetHtmlUrllib(url):
    "get html by urllib, now we don't use this because it can't render js."
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('UTF-8')
    return html

def GetHtml(url):
    "get html by requests-html which can render js."
    session=HTMLSession()
    s = session.get(url)
    # sleep 3 seconds ot wait other files rendered completely without js.
    # then render js script.
    s.html.render(sleep=3,wait=5, keep_page=True)
    return s.html.html

# def GetAllLinks(url, results):
#     html = GetHtml(url)
#     index_html = PQ(html)
#     links_html = index_html('.article-list div')
#     for x in links_html.items():
#         if x.attr('style') != "display: none;":
#             a_html = x('a')
#             href = a_html.attr('href')
#             if href:
#                 results.add(href)

def GetAllLinks(url, results):
    html = GetHtml(url)
    # print(html)
    index_html = PQ(html)
    a_html = index_html('.blog-index a')
    # print(index_html)
    for x in a_html.items():
        href = x.attr('href')
        print(href)
        if href:
            results.add(href)

res = set()
# driver=webdriver.PhantomJS()
# driver.get("https://thiefuniverse.github.io/")
# print(driver.page_source)

GetAllLinks("https://thiefuniverse.github.io/", res)
print(len(res))
