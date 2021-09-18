from __future__ import division

import os

from jinja2 import Template

from api.features.budget_commander.BudgetCommander import BudgetCommander
from api.features.budget_commander.pause_enable_campaigns.GetCostFromApi import \
    GetCostFromApi
from api.features.budget_commander.pause_enable_campaigns.PauseEnableCampaigns import \
    PauseEnableCampaigns
from api.Helpers import Helpers
from common.Email import Email
from common.helpers.LocalDates import LocalDates
from common.Log import Log
from common.Settings import Settings


class EmergencyStop(object):
    """
    * Will run hourly
    * Decides whether today's spend has spiked enough to warrant pausing campaigns
    * Re-enables campaigns if spend is under the limit
    """

    def __init__(self, account_id):
        self.account_id = account_id
        self.budget_commander = BudgetCommander(account_id)
        self.local_dates = LocalDates(account_id)
        if not self.budget_commander.user_settings['emergency_stop']:
            Log("info", "Emergency stop is disabled.", "", self.account_id)
            return
        self.budget = self.budget_commander.budget
        if self.budget_commander.this_month_spend >= self.budget:
            Log("info", "this month spend (%s) is over this month's budget (%s). Exiting." %(self.budget_commander.this_month_spend, self.budget), "", self.account_id)
            return
        self.costs = GetCostFromApi(account_id)
        self.today_cost = self.costs.today_cost
        self.day_budget_percentage = self.costs.day_budget_percentage
        self.day_limit = self.getDayLimit()
        self.main()
        
    def main(self):
        if not self.budget or self.budget==0:
            Log("info", "No budget set, cannot run emergency stop.", "", self.account_id)
            return

        Log("info", "today_cost: %s, day_limit: %s, budget: %s" %(self.today_cost, self.day_limit, self.budget), "", self.account_id)
        
        campaigns_are_enabled_day = self.budget_commander.campaignsAreEnabledDay()
        spend_is_over_emergency_limit = self.spendIsOverEmergencyLimit()
        if spend_is_over_emergency_limit and campaigns_are_enabled_day:
            (PauseEnableCampaigns(self.account_id)).pauseForToday()
            self.sendEmail()
            return

        campaigns_are_paused_day = self.budget_commander.campaignsArePausedDay()
        spend_is_under_emergency_limit = self.spendIsUnderEmergencyLimit()
        if spend_is_under_emergency_limit and campaigns_are_paused_day:
            (PauseEnableCampaigns(self.account_id)).enableForToday()
            return

        Log("info", "Emergency stop: no actions", "", self.account_id)

    def spendIsOverEmergencyLimit(self):
        if self.today_cost > self.day_limit:
            return True

        return False

    def spendIsUnderEmergencyLimit(self):
        if self.today_cost <= self.day_limit:
            return True

        return False

    def getDayLimit(self):
        """Get the day limit
        * The day budget based on day of the week phasing
        * Then multiply the phasing based on forecast Vs budget
        """

        if self.local_dates.is_first_of_month:
            vs_budget_multiplier = 1
        else:
            forecast = (self.budget_commander.this_month_spend/(self.local_dates.today.date().day-1))*self.local_dates.days_in_this_month
            vs_budget_multiplier = self.get_vs_budget_multiplier(self.budget_commander.this_month_spend, forecast)
        day_limit = self.budget * (self.day_budget_percentage*vs_budget_multiplier)
        minimum = self.budget/30.4
        if day_limit < minimum:
            day_limit = minimum

        return day_limit

    def get_vs_budget_multiplier(self, this_month_spend, forecast):
        if this_month_spend >= self.budget:
            return 0
        
        if forecast==0:
            return 1

        if self.budget==0:
            return 1

        vs_budget = self.budget/float(forecast)
        vs_budget_multiplier = vs_budget
        if vs_budget_multiplier > 3:
            vs_budget_multiplier = 3
        if vs_budget_multiplier < 0:
            vs_budget_multiplier = 0

        return vs_budget_multiplier


    def getHtmlContent(self):
        email_html_template = "budget_commander_emergency_stop_paused.html"

        template_path = os.path.abspath(os.path.join(Settings().python_dir,"email_templates", email_html_template))
        template = Template(open(template_path).read())

        html_content = template.render(
            username=self.budget_commander.username,
            account_name=self.budget_commander.name,
            account_id=self.budget_commander.account_id,
            google_account_id=self.budget_commander.google_id,
            day_limit=round(self.day_limit, 2),
            today_cost=round(self.today_cost, 2),
            currency_symbol=self.budget_commander.currency_symbol,
            )

        return html_content

    def sendEmail(self):
        subject = "Account '%s' (%s) | All Campaigns were paused for the rest of the day" % (self.budget_commander.name, self.budget_commander.google_id)

        html_content = self.getHtmlContent()

        email_addresses = self.budget_commander.getEmailAddresses()

        Log("info", "Sending email(s)", "%s - send to: %s" % (subject, ",".join(email_addresses),), self.account_id)
        assert len(email_addresses) > 0

        for email_address in email_addresses:
            # print email_address
            Email.send(("app@adevolver.com", "AdEvolver Budget Commander"), str(email_address), subject, html_content)
