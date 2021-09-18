# coding: utf-8
from __future__ import division

import calendar
import uuid
from datetime import datetime, timedelta

import pandas as pd

from api.Helpers import Helpers
from common.Database import Database
from common.helpers.Currency import Currency
from common.helpers.LocalDates import LocalDates
from common.Settings import Settings


class BudgetCommander(object):

    def __init__(self, account_id, budget_group_id=None):
        self.account_id = account_id
        self.local_dates = LocalDates(account_id)
        self.budget_group_id = budget_group_id
        self.budget_group_info = self.getBudgetGroupInfo()
        self.envvars = (Settings()).getEnv()
        self.createBudgetCommanderTable()
        self.account_info = self.getAccountInfo()
        self.name = self.account_info["name"]
        self.google_id = self.account_info["google_id"]
        self.currency_symbol = (Currency()).getSymbol(account_id)
        self.user_settings = self.getBudgetCommanderSettings()
        self.username = self.getUserName()
        self.budget = self.getBudget()
        self.this_month_spend = self.getThisMonthSpend()
        self.last_month_spend = self.getLastMonthSpend()
        self.under_budget = self.accountIsUnderBudget(
            self.budget, self.this_month_spend)

    def getBudget(self):
        if self.budget_group_id:
            budget = self.budget_group_info['budget']
        else:
            budget = self.account_info["budget"]

        if budget == "" or budget is None:
            print("No budget is set in the account. Can't run budget commander features")
            return None

        if self.user_settings["excess_budget"]:
            budget = budget + self.user_settings["excess_budget"]

        return float(budget)

    def getBudgetCommanderSettings(self):
        """
        Returns a dict of the budget commander settings
        """

        query = "select * from budget_commander where account_id = '%s'" % (self.account_id)
        data = pd.read_sql(query, (Database()).createEngine()).to_dict()

        user_settings = {}
        for key in data:
            try:
                user_settings[key] = data[key][0]
            except KeyError:
                return self.addDefaultBudgetCommanderSettings()

        return user_settings

    def getUserName(self):
        """
        Returns a dict of the user settings
        """

        query = """
        SELECT u.name FROM users as u
        join accounts as a
        on a.user_id = u.id
        where a.id = "%s"
        """ % (self.account_id)
        result = (Database()).createEngine().execute(query)

        for row in result:
            username = row[0]

        return username

    def addDefaultBudgetCommanderSettings(self):
        """If budget commander settings aren't availble add the defaults"""
        settings = {"1": {
            "id": uuid.uuid4(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "account_id": self.account_id,
            "notify_via_email": 0,
            "pause_campaigns": 0,
            "enable_campaigns": 0,
            "rollover_spend": 0,
            "control_spend": 0,
            "email_sent": 0,
            "emergency_stop": 0,
            "email_addresses": None,
            "day_paused_campaigns": None,
            "month_paused_campaigns": None,
            "excess_budget": None,
        }}

        # write to the db
        Database().appendRows("budget_commander", settings)

        return settings["1"]

    def campaignsAreEnabledDay(self):
        """Returns True if campaigns are enabled self.now i.e. under the Emergency Stop feature."""
        if not self.user_settings['day_paused_campaigns']:
            return True

        return False

    def campaignsArePausedDay(self):
        """Returns True if campaigns have been paused self.now i.e. under the Emergency Stop feature."""
        if self.user_settings['day_paused_campaigns']:
            return True

        return False

    def campaignsAreEnabledMonth(self):
        """Returns True if campaigns are enabled this month."""
        if not self.user_settings['month_paused_campaigns']:
            return True

        return False

    def campaignsArePausedMonth(self):
        """Returns True if campaigns have been paused this month."""
        if self.user_settings['month_paused_campaigns']:
            return True

        return False

    def getBudgetVsSpend(self, budget, this_month_spend):
        difference = this_month_spend - budget
        return difference

    def getBudgetVsSpendPercentage(self, budget, this_month_spend):
        difference = this_month_spend - budget
        percentage = difference / budget
        return percentage

    def getAccountInfo(self):
        query = "select budget, name,google_id,currency_code from accounts where id = '%s' " % (self.account_id)
        data = pd.read_sql(query, (Database()).createEngine()).to_dict()
        user_info = {}
        for key in data:
            user_info[key] = data[key][0]

        return user_info

    def getBudgetGroupInfo(self):
        #TODO replace with db call
        if not self.budget_group_id:
            return

        return {
            'budget':10000,
            'campaign_ids': [
                '0718ed0bd94066ecc0bb9547b987ca70',
                '0c9585ee582959565921a8526a234656',
                '3c2c13e31ae669c8a6848a9b96a8b62e',
                '3e1b976fbfd875257a3c11760a1267f6',
                '420a29b499d5c5c91ccbfdd4d28dc0a5',
                '434031658372f5d4908c2ffd4c279f9a',
                '4429a3b49a9139b7914bc5b5ab2c764d',
                '748dc2be28969766e707fd4c95c93510',
                '854527926988a5a2b92c9b6b5025d322',
                '96a2dc315ebf80b6696a5f973cfa1260',
                'af3b7fc51a61b7cbbac811b961ba5107',
                'b2a6e87e9fc8d213da014814690891cc',
                'fdcdd051326aa88723ecbfe1da8d5498'
            ]
        }


    def getThisMonthSpend(self):
        
        
        if self.local_dates.today.date().day == 1:
            return 0

        if self.budget_group_id:
            query = """
            select sum(cost) from campaign_performance where account_id = '%s'
            and date_range = 'THIS_MONTH'
            and campaign_id in (%s)
            """ %(self.account_id, ','.join(["'"+campaign_id+"'" for campaign_id in self.budget_group_info['campaign_ids']]))
            rows = Database().executeQuery(query)
            for row in rows:
                cost = row[0]
            if cost is None:
                return 0
            return cost

        query = "select sum(cost) from account_performance_reports where account_id = '%s' " % (self.account_id)
        query += " and date >= '%s' and date <= '%s' " % (self.local_dates.first_date_of_this_month, self.local_dates.yesterday)
        result = (Database()).createEngine().execute(query)
        for row in result:
            this_month_cost = row[0]
        
        if this_month_cost is None:
            return 0

        return this_month_cost

    def getLastMonthSpend(self):
        query = "select cost from account_performance_reports where account_id = '%s' " % (self.account_id)
        query += " and date >= '%s' and date <= '%s' " % (self.local_dates.first_date_of_last_month, self.local_dates.last_date_of_last_month)
        result = (Database()).createEngine().execute(query)
        last_month_cost = 0
        for row in result:
            last_month_cost += row[0]

        return last_month_cost

    def getSevenDaySpend(self):
        """Get cost from the last 7 days"""

        if self.local_dates.is_first_of_month:
            return 0

        query = "select cost from account_performance_reports where account_id = '%s' " % (self.account_id)
        query += " and date >= '%s' and date <= '%s' " % (self.local_dates.seven_days_ago, self.local_dates.yesterday)
        result = (Database()).createEngine().execute(query)
        cost = 0
        for row in result:
            cost += row[0]

        return cost

    def createBudgetCommanderTable(self):
        """Create budget commander table for testing.
        A migration will handle this in production"""

        if self.envvars["APP_ENV"] != "local":
            return

        if self.budgetCommanderTableExists():
            return

        columns = ["account_id", "email_sent", "email_addresses", "notify_via_email",
                   "pause_campaigns", "enable_campaigns", "control_spend", "rollover_budget", "day_paused_campaigns",
                   "month_paused_campaigns"]
        data = [[self.account_id, 0, "[charlesbannister@gmail.com, charles@adevolver.com]", 1, 0, 1, 1, 1, "", ""]]
        df = pd.DataFrame(data, columns=columns)
        df.to_sql(name="budget_commander", con=(Database()).createEngine(), index=False, if_exists="replace")

        with (Database()).createEngine().connect() as con:
            con.execute('alter table `budget_commander` modify account_id varchar(255)')
            con.execute('ALTER TABLE `budget_commander` ADD PRIMARY KEY (`account_id`);')

    def budgetCommanderTableExists(self):
        return True

    def accountIsUnderBudget(self, budget, this_month_spend):
        if budget is None or this_month_spend is None or this_month_spend >= budget:
            return False

        return True

    def getEmailAddresses(self):
        email_addresses = self.user_settings["email_addresses"]

        if email_addresses:
            email_addresses = email_addresses.strip('[]').replace('"', '').replace(' ', '').split(',')
        else:
            email_addresses = []

        query = """
        SELECT u.email FROM users as u
        join accounts as a 
        on a.user_id = u.id
        where a.id = "%s"
        """ % (self.account_id)
        result = (Database()).createEngine().execute(query)

        for row in result:
            user_email_address = row[0]
            if user_email_address != "":
                email_addresses.append(user_email_address)

        return list(set(email_addresses))  # return unique values only
