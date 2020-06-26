# -*- coding: utf-8 -*-

from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#https://stackoverflow.com/questions/50083638/export-scrapy-items-to-different-files
#https://stackoverflow.com/questions/29943075/scrapy-pipeline-to-export-csv-file-in-the-right-format
class FifaScrapyPipeline_Stats(object):
    def __init__(self):
        self.file = open("../data/players_stats.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
        # For csv file, use CsvItemExporter

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # def process_item(self, item, spider):
    #     return item

class FifaScrapyPipeline_URL(object):
    def __init__(self):
        self.file = open("../data/players_url.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item