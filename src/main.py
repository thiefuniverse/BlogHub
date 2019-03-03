#!usr/bin/env python3
# encoding: utf-8
from blog_detection import BlogDetector
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blog_config', required=True,
                        help="blog config file name.")
    parser.add_argument('-s', '--history_file',
                        required=True, help="history file name.")
    args = parser.parse_args()

    # crawl blog
    blog_detector = BlogDetector()
    # get current links craweled and new links
    result_links, all_new_links = blog_detector.DetectBlog(args.blog_config, args.history_file)
    print("all new links:", all_new_links)
    # save current links to history links for next craweling.
    blog_detector.SaveHistoryLinks(result_links, args.history_file)
    # if any new, notify someone.
    if all_new_links:
        blog_detector.Notify(all_new_links)
