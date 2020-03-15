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


def save_hrefs(href_list):
    with open(r"./detail_href_list_sorted_by_latest.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(href_list, ensure_ascii=False))


driver = webdriver.Chrome(executable_path="./chromedriver.exe")

href_list = None
with open(r"./detail_href_list_sorted_by_latest.json", "w", encoding="utf-8") as file:
    href_list = json.load(file.read())


for url in href_list:
    driver.get(url)
    title = driver.find_element_by_class_name("citation__title").text()
    authors = list()
    author_card = driver.find_element_by_id("sb-1")
    for i in author_card.find_elements_by_class_name("loa__item"):
        authors.append(i.text())
    publication = driver.find_element_by_class_name("epub-section__title").text()
    abstract = driver.find_element_by_class_name("hlFld-Abstract").text()
    references = list()
    refers = driver.find_elements_by_class_name("references__item")
    for refer in refers:
        references.append(refer.text())
    doc = get_empty_doc()
    doc["title"] = title
    doc["authors"] = authors
    doc["publication"] = publication
    doc["abstract"] = abstract
    doc["references"] = references
    next_page = driver.find_element_by_css_selector("a.pagination__btn--next")
    next_page.click()
    time.sleep(10)
