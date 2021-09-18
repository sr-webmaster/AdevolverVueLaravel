from __future__ import division

import os

from jinja2 import Template

from api.features.budget_commander.BudgetCommander import BudgetCommander
from api.features.budget_commander.pause_enable_campaigns.PauseEnableCampaigns import \
    PauseEnableCampaigns
from common.Database import Database
from common.Email import Email
from common.helpers.LocalDates import LocalDates
from common.Log import Log
from common.Settings import Settings


class MonthlyStop(object):
    """
    * Runs daily
    * Pauses campaigns if spend is over budget
    * Re-enables campaigns if spend is under the limit (e.g. new month)
    """

    def __init__(self, account_id):
        self.account_id = account_id
        self.local_dates = LocalDates(account_id)
        self.budget_commander = BudgetCommander(account_id)
        self.budget = self.budget_commander.budget
        self.cost = self.budget_commander.this_month_spend
        self.main()
    

    def main(self):
        self.store_excess_budget()

        if not self.budget_commander.user_settings["pause_campaigns"]:
            Log("info", "pause_campaigns is disabled", '', self.account_id)
            return

        campaigns_are_enabled_month = self.budget_commander.campaignsAreEnabledMonth()
        spend_is_over_budget = self.spendIsOverBudget()
        if spend_is_over_budget and campaigns_are_enabled_month:
            (PauseEnableCampaigns(self.account_id)).pauseForMonth()
            Log("info", "Budget commander monthly stop: campaigns paused for the month", "", self.account_id)
            self.sendEmail('Paused')
            return

        campaigns_are_paused_month = self.budget_commander.campaignsArePausedMonth()
        spend_is_under_budget = self.spendIsUnderBudget()
        if spend_is_under_budget and campaigns_are_paused_month and self.budget_commander.user_settings[
            "enable_campaigns"]:
            (PauseEnableCampaigns(self.account_id)).enableForMonth()
            Log("info", "Budget commander monthly stop: campaigns enabled for the month", "", self.account_id)
            self.sendEmail('Enabled')
            return

        Log("info", "Budget commander monthly stop: no actions", "", self.account_id)


    def getHtmlContent(self, new_status):
        if new_status=='Paused':
            email_html_template = "budget_commander_monthly_campaign_status_update_paused.html"
        if new_status=='Enabled':
            email_html_template = "budget_commander_monthly_campaign_status_update_enabled.html"

        template_path = os.path.abspath(os.path.join(Settings().python_dir,"email_templates", email_html_template))
        template = Template(open(template_path).read())

        html_content = template.render(
            username=self.budget_commander.username,
            account_name=self.budget_commander.name,
            account_id=self.budget_commander.account_id,
            google_account_id=self.budget_commander.google_id,
            budget=float(self.budget),
            spend=float(self.budget_commander.this_month_spend),
            currency_symbol=self.budget_commander.currency_symbol,
            new_status=new_status
            )

        return html_content

    def sendEmail(self, new_status):
        subject = "Account '%s' (%s) | All Campaigns were %s" % (self.budget_commander.name, self.budget_commander.google_id, new_status)

        html_content = self.getHtmlContent(new_status)

        email_addresses = self.budget_commander.getEmailAddresses()

        Log("info", "Sending email(s)", "%s - send to: %s" % (subject, ",".join(email_addresses),), self.account_id)
        assert len(email_addresses) > 0

        for email_address in email_addresses:
            # print email_address
            Email.send(("app@adevolver.com", "AdEvolver Budget Commander"), str(email_address), subject, html_content)

    def store_excess_budget(self):
        """Only run on the 1st of the month
        * - Take the budget
        * - Take away last month's spend
        * - Any remaining budget is stored as the excess
        """

        def update_excess_budget(excess_budget):
            Log('info', 'Storing excess budget', "excess_budget: %s" %(excess_budget), self.account_id)
            Database().setValue('budget_commander', 'excess_budget', excess_budget, 'where account_id = "%s"' %(self.account_id))

        if not self.budget_commander.user_settings['rollover_spend']:
            Log('info', 'rollover_spend is disabled. Setting excess to 0', '', self.account_id)
            update_excess_budget(0)
            return

        if not self.local_dates.is_first_of_month:
            return

        if self.budget_commander.budget_group_id:#no rollover for budget groups
            return

        remaining = float(self.budget) - float(self.budget_commander.last_month_spend)

        if remaining < 0:
            return 0

        update_excess_budget(remaining)

    def spendIsOverBudget(self):
        if self.cost > self.budget:
            return True

        return False

    def spendIsUnderBudget(self):
        if self.cost <= self.budget:
            return True

        return False
