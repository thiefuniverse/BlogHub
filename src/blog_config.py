#!usr/bin/env python3
# encoding: utf-8

import json

def checkKey(keys, dict):
    for key in keys:
        if key not in dict:
            return False
    return True
    
class CssSelector:
    def __init__(self):
        self.locate_filter = ""
        self.ignore_filter = dict()
        self.target_attribute = ""
    def print(self):
        print("css selector:")
        print("locate filter: ",self.locate_filter)
        print("ignore filter: ",self.ignore_filter)
        print("target attrbute: ",self.target_attribute)

class NextCssSelector:
    def __init__(self):
        self.CssSelector = CssSelector()
        self.next_css_selector = None

    def print(self):
        print("current next css selector:")
        self.CssSelector.print()
        fake_next = self.next_css_selector
        depth = 1
        while fake_next:
            print("current depth: ",depth)
            fake_next.CssSelector.print()
            fake_next = fake_next.next_css_selector
            depth += 1
        
class Config:
    def __init__(self):
        self.root_url = ""
        self.css_selector = CssSelector()
        self.next_css_selector = NextCssSelector()
        self.has_website_prefix = False

    def print(self):
        print("root_url:", self.root_url)
        self.css_selector.print()
        self.next_css_selector.print()
        print("has_website_prefix:", self.has_website_prefix)
    
    def ReadJsonDict(self, json_config):
        if not checkKey(["root_url", "has_website_prefix", "css_selector"], json_config):
            print("keys missing error in json_config.")
            return

        self.root_url = json_config["root_url"]
        self.has_website_prefix = json_config["has_website_prefix"]
        # get css selector
        css_selector_config = json_config["css_selector"]
        if css_selector_config:
            if "locate_filter" in css_selector_config:
                self.css_selector.locate_filter = css_selector_config["locate_filter"]
            if "target_attribute" in css_selector_config:
                self.css_selector.target_attribute = css_selector_config["target_attribute"]
            if "ignore_filter" in css_selector_config:
                self.css_selector.ignore_filter = css_selector_config["ignore_filter"]

            if "next_css_selector" in json_config:
                print("json tt:",json_config["next_css_selector"])
                self.next_css_selector =self.ReadNextCssSelector(self.next_css_selector, json_config["next_css_selector"])
        return 
   
    def ReadNextCssSelector(self, nes_selector, next_css_dict):
        if next_css_dict:
            # print("ncd:", next_css_dict)
            nes_selector = NextCssSelector()
            if "css_selector" in next_css_dict:
                css_select_dict = next_css_dict["css_selector"]
            if "locate_filter" in css_select_dict:
                nes_selector.CssSelector.locate_filter = css_select_dict["locate_filter"]
            if "ignore_filter" in css_select_dict:
                nes_selector.CssSelector.ignore_filter = css_select_dict["ignore_filter"]
            if "target_attribute" in css_select_dict:
                nes_selector.CssSelector.target_attribute = css_select_dict["target_attribute"]

            # print("nes selector cssselector:", nes_selector.print())
            ncs = ""
            if "next_css_selector" in next_css_dict:
                ncs = next_css_dict["next_css_selector"]
            if ncs:
                nes_selector.next_css_selector =self.ReadNextCssSelector(nes_selector.next_css_selector, ncs)
            return nes_selector
        return ""

    def Load(self, json_config_file):
        with open(json_config_file, "r", encoding='utf-8') as f:
            json_config = json.loads(f.read())
        self.ReadJsonDict(json_config)


# test 
if __name__ == "__main__":
    c = Config()
    c.Load("blog_index_selector/test_load_config.json")
    c.print()
    print("****************************************")


