#!usr/bin/env python3
# encoding: utf-8

from blog_crawler import Crawler
from blog_config import Config, JsonReader
from blog_markdown import MarkdownBuilder
import argparse, re

# number of words limit
content_max_limit = 400

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link_file', required=True,
                        help="one file which contains new links.")
    parser.add_argument('-t', '--title_config',
                        required=True, help="blog title config json file.")
    parser.add_argument('-e', '--template_file',
                        required=True, help="template file which will be used to generate commit info.")
    parser.add_argument('-s', '--save_file',
                        required=True, help="save markdown file.")
    args = parser.parse_args()

    # get all new links
    with open(args.link_file) as f:
        all_links = f.readlines()

    target_title_json = JsonReader()
    target_title_json.addJsonFile(args.title_config)
    crawler_blog = Crawler()
    blog_markdowner = MarkdownBuilder()

    for link in all_links:
        link = link.strip()
        # set current link
        target_title_json.updateJson({"root_url":link})
        link_config = Config()
        link_config.ReadJsonDict(target_title_json.getJson())
        # get current title
        results, html_text = crawler_blog.GetAllTargets(link_config)

        current_dict = {}
        if len(results) > 0:
            print("current target: ", results)
            current_title = results[0]
            current_dict = target_title_json.getJson()
            current_dict["blog_title"] = current_title
            current_dict["blog_url"] = link
            html_text = re.sub("<.*>","", html_text)
            html_text = re.sub("/\*.*/","", html_text)
            print("html_text:", html_text[:content_max_limit])
            html_content = html_text[:content_max_limit]+"..."
            html_content.replace("\n", "")
            current_dict["blog_content"] = html_content 
            blog_markdowner.renderTemplateFile(args.template_file, current_dict)
            blog_markdowner.saveFile(args.save_file)
        else:
            print("error for crawler_blog GetAllTargets.")