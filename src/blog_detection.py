#!usr/bin/env python3
# encoding: utf-8

from blog_config import Config
from blog_crawler import Crawler
import sys, json
from collections import OrderedDict

class BlogDetector:
    def __init__(self):
        self.crawler = Crawler()
        self.config = Config()

    def DetectBlog(self, blog_config_file, history_links_file):
        "detect whether blog has some update or not."
        if blog_config_file:
            self.config.Load(blog_config_file)
        else:
            print("blog config file is empty. args error!")
            return
        result_links = set()
        # we need catch exception
        result_links = set(self.crawler.GetAllLinks(self.config))

        # read history links
        with open(history_links_file, "r", encoding='utf-8') as f:
            history_links_json= json.loads(f.read())
        history_links = set(history_links_json["history_links"])
        
        # get new blog links
        if not self.config.has_website_prefix:
            result_links = set(self.config.root_url+"/"+x for x in result_links)
        new_blog_links = set()
        for link in result_links:
            if link not in history_links:
                new_blog_links.add(link)

        return result_links, new_blog_links

    def SaveHistoryLinks(self, result_links, history_file):
        res = dict()
        res["history_links"] = []
        for link in result_links:
            res["history_links"].append(link)
        # sorted(res["history_links"])
        # write file
        with open(history_file, "w", encoding='utf-8') as f:
            f.write(json.dumps(res, indent=4, sort_keys=False))

    def SaveNewLinks(self, new_links, new_links_file):
        # write file
        with open(new_links_file, "w", encoding='utf-8') as f:
            for link in new_links:
                f.write(link+"\n")

if __name__ == "__main__":
    # todo 
    # optimize args input, use args_parser
    if len(sys.argv) < 3:
        print("args error")
        exit
    blogdetector = BlogDetector()
    result_links, all_new_links = blogdetector.DetectBlog(sys.argv[1], sys.argv[2])
    blogdetector.SaveHistoryLinks(result_links, sys.argv[2])
    if all_new_links:
        blogdetector.SaveNewLinks(all_new_links, "new_links.json")
    
    d = ["a.html", "b.html"]
    c = []
    blogdetector.SaveNewLinks(d, "d.json")
    blogdetector.SaveNewLinks(c, "c.json")