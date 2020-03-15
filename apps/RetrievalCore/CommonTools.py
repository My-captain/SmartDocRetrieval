# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 12:04
# @Author  : Mr.Robot
# @Site    : 
# @File    : CommonTools.py
# @Software: PyCharm


def get_vector_space_by_doc(doc, vocabulary):
    """
    计算文档实体的向量空间
    :param doc: 传入的文档实体
    :param vocabulary: 词库内容（dict<word:IDF>）
    :return: 该文档的向量空间
    """
    pass


def initial_d_p_vector(type_num):
    """
    初始化D&P
    :param type_num: 类别个数
    :return: D/P向量
    """
    pass


def update_d_value(origin_d_vector, current_vector):
    """
    更新d值
    :param origin_d_vector: 原d值向量 list<float>
    :param current_vector: 当前用户打分向量 list<float>
    :return: 更新后的d值向量
    """
    pass


def update_p_value(origin_p_vector, current_vector):
    """
    更新p值
    :param origin_p_vector: 原p值向量 list<float>
    :param current_vector: 当前用户打分向量 list<float>
    :return: 更新后的p值向量
    """
    pass


def sort_docs_by_dp(doc_list, d_vector, p_vector):
    """
    根据D/P向量对文献列表进行排序
    :param doc_list: list<DocModel>
    :param d_vector: d值向量
    :param p_vector: p值向量
    :return: list<DocModel>
    """
    pass

