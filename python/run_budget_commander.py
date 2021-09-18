import argparse
import traceback

import requests

from api.features.budget_commander.ControlSpend import ControlSpend
from api.features.budget_commander.NotifyViaEmail import NotifyViaEmail
from api.features.budget_commander.pause_enable_campaigns.MonthlyStop import \
    MonthlyStop
from api.Helpers import Helpers
# from api.features.budget_commander.PauseEnableCampaigns import PauseEnableCampaigns
from common.Log import Log


def main():
    """Run each morning after data processing has occured
     - This is triggered to run after every_night.py
     """

    parser = argparse.ArgumentParser()
    parser.add_argument("-a")
    args = parser.parse_args()

    try:
        account_id = args.a
        if(not account_id):
            print('Please specify an account id with -a')
            return
        if not Helpers().isActiveAccount(account_id):
            Log("info", "this account isn't active. Exiting", '', account_id)
            return
        NotifyViaEmail(account_id).main()
        MonthlyStop(account_id)
        
        ControlSpend(account_id).main()
        
    # TODO: catch proper exception
    except:
        Log("error", "error starting run_budget_commander.py from command line", traceback.format_exc())
        # TODO: return proper exception
        raise


if __name__ == '__main__':
    requests.get('http://beats.envoyer.io/heartbeat/QzelTxLzy11oVGz')
    main()
