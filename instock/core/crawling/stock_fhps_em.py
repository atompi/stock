#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/4/7 15:22
Desc: 东方财富网-数据中心-年报季报-分红送配
https://data.eastmoney.com/yjfp/
"""
import pandas as pd
import requests
from tqdm import tqdm

__author__ = 'myh '
__date__ = '2023/6/27 '

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}


def stock_fhps_em(date: str = "20231231") -> pd.DataFrame:
    """
    东方财富网-数据中心-年报季报-分红送配
    https://data.eastmoney.com/yjfp/
    :param date: 分红送配报告期
    :type date: str
    :return: 分红送配
    :rtype: pandas.DataFrame
    """
    import warnings

    warnings.simplefilter(action="ignore", category=FutureWarning)

    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "sortColumns": "PLAN_NOTICE_DATE",
        "sortTypes": "-1",
        "pageSize": "500",
        "pageNumber": "1",
        "reportName": "RPT_SHAREBONUS_DET",
        "columns": "ALL",
        "quoteColumns": "",
        "js": '{"data":(x),"pages":(tp)}',
        "source": "WEB",
        "client": "WEB",
        "filter": f"""(REPORT_DATE='{"-".join([date[:4], date[4:6], date[6:]])}')""",
    }

    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    total_pages = int(data_json["result"]["pages"])
    big_df = pd.DataFrame()
    for page in tqdm(range(1, total_pages + 1), leave=False):
        params.update({"pageNumber": page})
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["result"]["data"])
        if not temp_df.empty:
            big_df = pd.concat(objs=[big_df, temp_df], ignore_index=True)

    big_df.columns = [
        "_",
        "名称",
        "_",
        "_",
        "代码",
        "送转股份-送转总比例",
        "送转股份-送转比例",
        "送转股份-转股比例",
        "现金分红-现金分红比例",
        "预案公告日",
        "股权登记日",
        "除权除息日",
        "_",
        "方案进度",
        "_",
        "最新公告日期",
        "_",
        "_",
        "_",
        "每股收益",
        "每股净资产",
        "每股公积金",
        "每股未分配利润",
        "净利润同比增长",
        "总股本",
        "_",
        "现金分红-股息率",
        "-",
        "-",
        "-",
    ]
    big_df = big_df[
        [
            "代码",
            "名称",
            "送转股份-送转总比例",
            "送转股份-送转比例",
            "送转股份-转股比例",
            "现金分红-现金分红比例",
            "现金分红-股息率",
            "每股收益",
            "每股净资产",
            "每股公积金",
            "每股未分配利润",
            "净利润同比增长",
            "总股本",
            "预案公告日",
            "股权登记日",
            "除权除息日",
            "方案进度",
            "最新公告日期",
        ]
    ]
    big_df["送转股份-送转总比例"] = pd.to_numeric(big_df["送转股份-送转总比例"], errors="coerce")
    big_df["送转股份-送转比例"] = pd.to_numeric(big_df["送转股份-送转比例"], errors="coerce")
    big_df["送转股份-转股比例"] = pd.to_numeric(big_df["送转股份-转股比例"], errors="coerce")
    big_df["现金分红-现金分红比例"] = pd.to_numeric(big_df["现金分红-现金分红比例"], errors="coerce")
    big_df["现金分红-股息率"] = pd.to_numeric(big_df["现金分红-股息率"], errors="coerce")
    big_df["每股收益"] = pd.to_numeric(big_df["每股收益"], errors="coerce")
    big_df["每股净资产"] = pd.to_numeric(big_df["每股净资产"], errors="coerce")
    big_df["每股公积金"] = pd.to_numeric(big_df["每股公积金"], errors="coerce")
    big_df["每股未分配利润"] = pd.to_numeric(big_df["每股未分配利润"], errors="coerce")
    big_df["净利润同比增长"] = pd.to_numeric(big_df["净利润同比增长"], errors="coerce")
    big_df["总股本"] = pd.to_numeric(big_df["总股本"], errors="coerce")

    big_df["预案公告日"] = pd.to_datetime(big_df["预案公告日"], errors="coerce").dt.date
    big_df["股权登记日"] = pd.to_datetime(big_df["股权登记日"], errors="coerce").dt.date
    big_df["除权除息日"] = pd.to_datetime(big_df["除权除息日"], errors="coerce").dt.date
    big_df["最新公告日期"] = pd.to_datetime(big_df["最新公告日期"], errors="coerce").dt.date
    big_df.sort_values(["最新公告日期"], inplace=True, ignore_index=True)
    return big_df


if __name__ == "__main__":
    stock_fhps_em_df = stock_fhps_em(date="20221231")
    print(stock_fhps_em_df)
