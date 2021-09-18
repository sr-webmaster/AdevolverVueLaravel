# -*- coding: utf-8 -*-
from __future__ import division

import os

from jinja2 import Template

from api.features.budget_commander.BudgetCommander import BudgetCommander
from common.Database import Database
from common.Email import Email
from common.Log import Log
from common.Settings import Settings


class NotifyViaEmail(BudgetCommander):

    def __init__(self, account_id):
        BudgetCommander.__init__(self, account_id)
        self.account_id = account_id

    def main(self):

        if self.user_settings["pause_campaigns"]:
            print("paused campaigns is enabled. Exiting...")
            return  # they'll get an email when the campaigns pause so there's no need to send one here
        print("running email notifier")

        if self.budget is None:
            return

        print("under_budget: " + str(self.under_budget))

        print("email_sent: " + str(self.user_settings["email_sent"]))

        if not self.user_settings["notify_via_email"]:
            Log("info", "email notifications turned off", '', self.account_id)
            return

        if self.under_budget and self.user_settings["email_sent"]:
            self.markAsNotSent()
            return

        if not self.user_settings["email_sent"] and not self.under_budget:
            self.sendEmail()
            return

        Log("info", "no action", "NotifyViaEmail", self.account_id)

    def markAsSent(self):
        # update the budget_commander table mark the account's email as sent
        # email_sent field
        print("marking as sent")
        query = "update budget_commander set email_sent = 1 where account_id = '%s' " % (self.account_id)
        (Database()).createEngine().execute(query)

    def markAsNotSent(self):
        print("marking as not sent...")
        query = "update budget_commander set email_sent = 0 where account_id = '%s' " % (self.account_id)
        (Database()).createEngine().execute(query)

    def getHtmlContent(self):
        template_path = os.path.abspath(os.path.join(Settings().python_dir,"email_templates", "budget_commander_email_notification.html"))
        template = Template(open(template_path).read())

        html_content = template.render(
            username=self.username,
            account_name=self.name,
            account_id=self.account_id,
            google_account_id=self.google_id,
            budget=float(self.budget),
            spend=float(self.this_month_spend),
            currency_symbol=self.currency_symbol,
            )

        return html_content

    def sendEmail(self):
        subject = "Account '%s' (%s) has gone over budget" % (self.name, self.google_id)

        html_content = self.getHtmlContent()

        email_addresses = self.getEmailAddresses()

        Log("info", "Sending email(s)", "%s - send to: %s" % (subject, ",".join(email_addresses),), self.account_id)
        assert len(email_addresses) > 0

        for email_address in email_addresses:
            # print email_address
            Email.send(("app@adevolver.com", "AdEvolver Budget Commander"), str(email_address), subject, html_content)

        self.markAsSent()
