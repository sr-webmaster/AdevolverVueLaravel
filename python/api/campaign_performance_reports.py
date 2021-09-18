# coding: utf-8
from __future__ import division

import warnings

import common.functions as functions
from api.Report import Report
from common.Log import Log

warnings.filterwarnings("ignore")

options = {
    "report_name": "CAMPAIGN_PERFORMANCE_REPORT",
    "performance_table_name": "campaign_performance",
    "entity_table_name": "campaigns",
    "entity_id_name": "campaign_id",

    "where_string": " where CampaignStatus = ENABLED and CampaignTrialType = BASE and AdNetworkType1 = SEARCH and AdNetworkType2 = SEARCH ",

    "queryColumnsToTableColumns": {
        'CampaignId': "google_id",
        'Cost': "cost",
        'Impressions': "impressions",
        'Conversions': "conversions",
        'Clicks': "clicks",
        'ConversionValue': "conversion_value",
        'CampaignName': 'name',
        'CampaignStatus': 'status',
    },

    # map query column name to downloaded column names
    "queryColumnsToDownloadColumns": {
        'CampaignId': "Campaign ID",
        'Cost': "Cost",
        'Impressions': "Impressions",
        'Conversions': "Conversions",
        'Clicks': "Clicks",
        'ConversionValue': "Total conv. value",
        'CampaignName': "Campaign",
        'CampaignStatus': "Campaign state",
    }

}


def main(account_id):
    Log("info", "getting campaign performance from the api", "", account_id)

    report = Report(account_id, "", options)

    df = report.createDfWithAllDateRanges(account_id)

    if functions.dfIsEmpty(df):
        return

    # remember column headers are as per the download here
    df["campaign_id"] = df.apply(lambda row: functions.addIdToDf(account_id, row["Campaign ID"]), axis=1)
    df["id"] = df["campaign_id"]

    df = report.basicProcessing(df)

    report.writeToEntitiesTable(df, report, account_id)

    report.writeToPerformanceTable(df, report, account_id)
