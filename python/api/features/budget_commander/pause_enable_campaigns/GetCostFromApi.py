#!/usr/bin/env python
from __future__ import division

import requests
from google.auth.exceptions import TransportError
from datetime import datetime, timedelta

from api.Helpers import Helpers
from api.Report import Report
from common.Settings import Settings
from common.helpers.LocalDates import LocalDates

options = {
    "report_name": "ACCOUNT_PERFORMANCE_REPORT",
    "performance_table_name": "account_performance",
    "entity_table_name": "accounts",
    "entity_id_name": "account_id",

    "where_string": " ",

    "queryColumnsToTableColumns": {
        'Cost': "cost",
        'Date': "date",
    },

    # map query column name to downloaded column names
    "queryColumnsToDownloadColumns": {
        'Cost': "Cost",
        'Date':'Date',
    }

}


class GetCostFromApi(object):
    """
        Downloads api data for both today and the previous 28 days (28 because we need 4 whole weeks)
        Used in emergency stop budget calculations
    """

    def __init__(self, account_id):
        self.account_id = account_id
        self.local_dates = LocalDates(account_id)
        self.df = self.main(account_id)
        self.today_cost = self.getTodayCost()
        self.day_budget_percentage = self.getBudgetPercentage()
        

    def main(self, account_id):

        if (Settings()).envvars["APP_DEBUG"] == "true":
            return 1

        date_range = self.getDateRange()

        report = Report(account_id, date_range, options)

        report.createAccountDirectory()

        report.createReportDirectory()

        try:
            report.downloadReport(account_id, options["where_string"])
        except requests.exceptions.ConnectionError:
            print("NO INTERNET CONNECTION")
            if Settings().envvars["APP_ENV"]=='production':
                raise
            return 1000
        except TransportError:
            print("NO INTERNET CONNECTION")
            if Settings().envvars["APP_ENV"]=='production':
                raise
            return 1000

        df = report.convertCsvToDataframe()

        df['Cost'] = df['Cost'] / 1000000

        df = df.sort_values('Day')
        df = df.reset_index()

        return df

    def getBudgetPercentage(self):
        """Get today's budget percentage based on today's previous spend Vs average"""
        def weekday(date):
            date = datetime.strptime(date, '%Y-%m-%d')
            return date.weekday()

        last_four_weeks_df = self.df.drop(28)#exclude today
        last_four_weeks_df['weekday'] = last_four_weeks_df['Day'].apply(lambda date: weekday(date))

        last_four_weeks_df = last_four_weeks_df.groupby('weekday').sum()
        last_four_weeks_df['average_day'] = last_four_weeks_df['Cost']/4
        last_four_weeks_df['day_percentage_of_total'] = last_four_weeks_df['average_day']/last_four_weeks_df['Cost'].sum()
        
        return last_four_weeks_df[last_four_weeks_df.index==self.local_dates.today.weekday()].day_percentage_of_total.values[0]

    def getTodayCost(self):
        return self.df[self.df.index==28].Cost.values[0]

    def getDateRange(self):
        start_date = str((self.local_dates.today - timedelta(28)).strftime('%Y%m%d'))
        end_date= str(self.local_dates.today.strftime('%Y%m%d'))
        return '%s,%s'%(start_date, end_date)
