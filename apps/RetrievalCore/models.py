from django.db import models
import json

# Create your models here.


class Document(models.Model):
    title = models.CharField(max_length=2048, verbose_name="文献标题", null=False, blank=False)
    publish_year = models.IntegerField(default=2019, verbose_name="发布年份")
    authors = models.TextField(verbose_name="作者列表")
    abstract = models.TextField(verbose_name="文献摘要")
    doi_url = models.TextField(verbose_name="原文详情页链接")
    references = models.TextField(verbose_name="引用列表")
    publication = models.TextField(verbose_name="文献发表信息")
    classification = models.IntegerField(verbose_name="所属类别", default=-1, null=True, blank=True)

    class Meta:
        verbose_name = "文献"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_authors(self):
        """
        获取当前文献的所有作者
        :return: List<author>
        """
        author_list = json.loads(self.authors)
        return author_list

    def get_references(self):
        """
        获取当前文献的所有引用列表
        :return: List<reference>
        """
        author_list = json.loads(self.authors)
        return author_list


class Session(models.Model):
    D_vector = models.TextField(verbose_name="D向量")
    P_vector = models.TextField(verbose_name="P向量")
    precision = models.FloatField(verbose_name="此此session的准确率")

    class Meta:
        verbose_name = "会话"
        verbose_name_plural = verbose_name

    def get_D_vector(self):
        """
        获取当前会话的D向量
        :return: List<D_i>
        """
        D = json.loads(self.D_vector)
        return D

    def get_references(self):
        """
        获取当前会话的P向量
        :return: List<P_i>
        """
        P = json.loads(self.P_vector)
        return P
