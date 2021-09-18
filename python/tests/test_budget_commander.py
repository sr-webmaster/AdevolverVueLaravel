import unittest

from api.features.budget_commander.BudgetCommander import BudgetCommander


class TestBudgetCommander(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBudgetCommander, self).__init__(*args, **kwargs)
        self.account_id = "f24c250e-b71a-4f48-acdb-a02637ab76f6"
    #
    # def test_create_table(self):
    #     (BudgetCommander(self.account_id)).createBudgetCommanderTable()

    # def test_account_under_budget_equal_values(self):
    #     budget = 10000
    #     this_month_spend = 10000
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #     result = (budget_commander).accountIsUnderBudget(budget, this_month_spend)
    #     self.assertFalse(result)

    # def test_account_under_budget_budget_under(self):
    #     budget = 9000
    #     this_month_spend = 10000
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #     result = (budget_commander).accountIsUnderBudget(budget, this_month_spend)
    #     self.assertFalse(result)

    # def test_account_under_budget_budget_over(self):
    #     budget = 10000
    #     this_month_spend = 9999
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #     result = (budget_commander).accountIsUnderBudget(budget, this_month_spend)
    #     self.assertTrue(result)

    # def test_budget_vs_spend_equal_spend(self):
    #     budget = 10000
    #     this_month_spend = 10000
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #
    #     result = budget_commander.getBudgetVsSpend(budget, this_month_spend)
    #     self.assertEquals(result, 0)

    # def test_budget_vs_spend_budget_higher(self):
    #     budget = 10001
    #     this_month_spend = 10000
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #
    #     result = budget_commander.getBudgetVsSpend(budget, this_month_spend)
    #     self.assertEquals(result, -1)

    # def test_budget_vs_spend_percentage_budget_higher(self):
    #     budget = 10
    #     this_month_spend = 9
    #
    #     budget_commander = BudgetCommander(self.account_id)
    #
    #     result = budget_commander.getBudgetVsSpendPercentage(budget, this_month_spend)
    #     self.assertEquals(result, -.1)
