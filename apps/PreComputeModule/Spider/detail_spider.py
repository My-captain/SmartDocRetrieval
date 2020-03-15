# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 15:14
# @Author  : Mr.Robot
# @Site    : 
# @File    : detail_spider.py
# @Software: PyCharm

import json
import time
from selenium import webdriver


def get_empty_doc():
    return {
        "title": None,
        "authors": None,
        "publication": None,
        "abstract": None,
        "references": None
    }


def save_detail(href_list):
    with open(r"./doc_detail.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(href_list, ensure_ascii=False))


driver = webdriver.Chrome('./chromedriver')

href_list = None
with open(r"./detail_href_list_sorted_by_latest.json", "r", encoding="utf-8") as file:
    file_content = file.read()
    href_list = json.loads(file_content)

detail_list = list()

for url in href_list[1646:]:
    while True:
        try:
            driver.get(url)
            title = driver.find_element_by_class_name("citation__title").text
            authors = list()
            author_card = driver.find_element_by_id("sb-1")
            for i in author_card.find_elements_by_class_name("loa__item"):
                authors.append(i.text)
            publication = driver.find_element_by_class_name("epub-section__title").text
            abstract = driver.find_element_by_class_name("hlFld-Abstract").text
            references = list()
            refers = driver.find_elements_by_class_name("references__item")
            for refer in refers:
                references.append(refer.text)
            break
        except Exception as e:
            print("出现异常")
            time.sleep(0.8)
    doc = get_empty_doc()
    doc["title"] = title
    doc["authors"] = authors
    doc["publication"] = publication
    doc["abstract"] = abstract
    doc["references"] = references
    detail_list.append(doc)
    save_detail(detail_list)
    time.sleep(1)
