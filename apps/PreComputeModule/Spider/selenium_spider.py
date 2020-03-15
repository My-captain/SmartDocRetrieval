# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 13:58
# @Author  : Mr.Robot
# @Site    : 
# @File    : selenium_spider.py
# @Software: PyCharm

import json
import time
from selenium import webdriver


driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver.get("https://dl.acm.org/action/doSearch?ConceptID=80&target=ccs-topics")


def save_hrefs(href_list):
    with open(r"./detail_href_list_sorted_by_latest.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(href_list, ensure_ascii=False))


href_list = list()
while True:

    cards = driver.find_elements_by_class_name("issue-item-container")
    for card in cards:
        href = card.find_element_by_class_name("issue-item__title").find_element_by_tag_name("a").get_property("href")
        href_list.append(href)
    save_hrefs(href_list)

    next_page = driver.find_element_by_css_selector("a.pagination__btn--next")
    next_page.click()
    time.sleep(10)

