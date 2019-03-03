#!usr/bin/env python3
# encoding: utf-8

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
        # sleep 6 seconds ot wait other files rendered completely without js.
        # then render js script.
        s.html.render(sleep=6,wait=5, keep_page=True)
        return s.html.html

    def GetAllLinks(self, config):
        if config.root_url:
            html = self.GetHtml(config.root_url)
        else:
            print("config.root_url is empty. whoopos error!")
            return
        # test function
        # html = open("test_json_selector.html", "r").read()
        results = self.RecursionCssSelector(config.css_selector, config.next_css_selector, html)
        return results

    def RecursionCssSelector(self, css_select, next_css_select, current_html):
        if not css_select:
            return []
        cur_css_html = PQ(current_html)
        css_htmls = cur_css_html(css_select.locate_filter)
        res = []

        # ignore some htmls by ignore_filter
        ignore_attr_dict = css_select.ignore_filter
        target_attr = css_select.target_attribute

        # get sub html elements
        if ignore_attr_dict:
            for one_html in css_htmls.items():
                for k in ignore_attr_dict:
                    if not one_html.attr(k) == ignore_attr_dict[k]:
                        res.append(one_html.html())
        else:
            for one_html in css_htmls.items():
                res.append(one_html.html())      

        # if current css selector has target attribute, then we extract target link directly.
        res_real = []
        if target_attr:
            for one_html in css_htmls.items():
                ta = one_html.attr(target_attr)
                if ta:
                    print("get one a:", ta)
                    res_real.append(ta)
            
        # handle next css selector
        result = []
        if next_css_select:
            for res_html in res:
                recursion_res = []
                if res_html and next_css_select.CssSelector:
                    recursion_res = self.RecursionCssSelector(next_css_select.CssSelector, next_css_select.next_css_selector, res_html)
                if recursion_res:
                    result += recursion_res
        result += res_real
        # print("current result done:", result)
        return result



# test 
if __name__ == "__main__":
    craw = Crawler()
    c = Config()
    c.Load("blog_index_selector/csdn.def.json")

    res = set()
    c.print()
    res = set(craw.GetAllLinks(c))
    print(len(res))
