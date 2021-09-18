# coding: utf-8
from api.features.budget_commander.BudgetCommander import BudgetCommander
from api.features.budget_commander.pause_enable_campaigns.PauseCampaigns import PauseCampaigns
from api.mutations_queue.CampaignStatusChange import CampaignStatusChange
from common.Database import Database
from common.Settings import Settings


class PauseEnableCampaigns(object):
    """
    * Accepts whether it's the day or month pause
    * Pauses or Enables campaigns
    """

    def __init__(self, account_id):
        self.account_id = account_id
        self.envvars = (Settings()).getEnv()
        self.budget_commander = BudgetCommander(account_id)
        self.user_settings = self.budget_commander.user_settings

    def main(self):
        print("running campaign pauser enabler")

        # self.createBudgetCommanderTable()

        if self.user_settings["enable_campaigns"] and self.campaignsPaused() and self.budget_commander.under_budget:
            self.enableCampaigns()
            self.notifyCampaignsEnabled()
            print("return 1")
            return

        if self.campaignsPaused():
            print("return 2")
            return

        if self.user_settings["pause_campaigns"] and not self.budget_commander.under_budget:
            (PauseCampaigns(self.account_id))
            # self.notifyCampaignsPaused()
            return

        print("no action")

    def pauseForToday(self):
        """Pause all campaigns and store their IDs."""
        campaign_ids = self.getActiveCampaignIds()
        CampaignStatusChange(self.account_id, campaign_ids, 'PAUSED')
        self.setDayPausedCampaigns(campaign_ids)

    def pauseForMonth(self):
        """Pause all campaigns and store their IDs."""
        campaign_ids = self.getActiveCampaignIds()
        CampaignStatusChange(self.account_id, campaign_ids, 'PAUSED')
        self.setMonthPausedCampaigns(campaign_ids)

    def getActiveCampaignIds(self):
        query = """
        SELECT google_id,id from campaigns
        WHERE account_id = '%s'
        AND status = 'enabled'
        """ % (self.account_id)
        result = (Database()).executeQuery(query)
        campaign_ids = []
        for row in result:
            campaign_ids.append(row)

        return campaign_ids

    def setDayPausedCampaigns(self, campaign_ids):
        """Stores campaign ids under the day_paused_campaigns column.
        
        Arguments:
        campaign_ids -- list of campaign ids which have been paused
        """

        table_name = "budget_commander"
        column = "day_paused_campaigns"
        where_string = 'where account_id = "%s"' % (self.account_id)
        campaign_ids = ['|'.join(campaign_id) for campaign_id in campaign_ids]
        (Database()).setValue(table_name, column, ",".join(campaign_ids), where_string)

    def setMonthPausedCampaigns(self, campaign_ids):
        """Stores campaign ids under the month_paused_campaigns column.
        
        Arguments:
        campaign_ids -- list of campaign ids which have been paused. Tuple containing (google_id, entity_id)
        """

        table_name = "budget_commander"
        column = "month_paused_campaigns"
        where_string = 'where account_id = "%s"' % (self.account_id)
        campaign_ids = ['|'.join(campaign_id) for campaign_id in campaign_ids]
        (Database()).setValue(table_name, column, ",".join(campaign_ids), where_string)

    def setDayPausedCampaignsToNull(self):
        """Sets the day_paused_campaigns value to null for this account"""
        table_name = "budget_commander"
        column = "day_paused_campaigns"
        where_string = 'where account_id = "%s"' % (self.account_id)
        (Database()).setValue(table_name, column, "", where_string)

    def setMonthPausedCampaignsToNull(self):
        """Sets the month_paused_campaigns value to null for this account"""
        table_name = "budget_commander"
        column = "month_paused_campaigns"
        where_string = 'where account_id = "%s"' % (self.account_id)
        (Database()).setValue(table_name, column, "", where_string)

    def enableForToday(self):
        """Enable campaigns based on stored IDs. Remove the IDs."""
        campaign_ids = self.user_settings['day_paused_campaigns']
        campaign_ids = [campaign_id.split('|') for campaign_id in campaign_ids.split(',')]
        CampaignStatusChange(self.account_id, campaign_ids, 'ENABLED')
        self.setDayPausedCampaignsToNull()

    def enableForMonth(self):
        """Enable campaigns based on stored IDs. Remove the IDs."""
        campaign_ids = self.user_settings['month_paused_campaigns']
        campaign_ids = [campaign_id.split('|') for campaign_id in campaign_ids.split(',')]
        CampaignStatusChange(self.account_id, campaign_ids, 'ENABLED')
        self.setMonthPausedCampaignsToNull()

    def campaignsPaused(self):
        result = self.user_settings["paused_campaign_ids"]
        if result == "" or result is None:
            return False

        return True

    def enableCampaigns(self):
        pass
        # get campaign ids
        # enable campaigs with those ids

    def notifyCampaignsEnabled(self):
        pass
        # send an email "campaigns re-enabled!"

    def notifyCampaignsPaused(self):
        pass
        # send an email "campaigns paused!"

    def getRollover(self):
        pass

    def setRollover(self):
        pass
        # based on last month's budget and spend
