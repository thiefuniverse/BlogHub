#!/bin/python3

import json

class Config:
    def __init__(self):
        self.root_url = ""
        self.css_selector = ""
        self.has_website_prefix = False

    def print(self):
        print("root_url:", self.root_url)
        print("css_selector:", self.css_selector)
        print("has_website_prefix:", self.has_website_prefix)

    def Load(self, json_config_file):
        with open(json_config_file, "r", encoding='utf-8') as f:
            json_config = json.loads(f.read())
        self.root_url = json_config["root_url"]
        self.css_selector = json_config["css_selector"]
        self.has_website_prefix = json_config["has_website_prefix"]


# test 
if __name__ == "__main__":
    c = Config()
    c.Load("blog_index_selector/csdn.def.json")
    c.print()