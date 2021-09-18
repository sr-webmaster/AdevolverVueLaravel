<?php

namespace App\Http\Controllers\api;

use App\Http\Resources\AccountBCGraphResource;
use App\Models\Account;
use App\Http\Controllers\Controller;
use Carbon\Carbon;

class AccountBudgetCommanderGraph extends Controller
{

    public function show(Account $account)
    {

        $account->performance;
        $after_date = Carbon::now()->startOfMonth()->previous('day')->toDateTimeString();
        $account_performance_reports = $account->account_performance_report->where('date', '>', $after_date);
        $account->this_month_performance = [
            'conversions' => $account_performance_reports->pluck('conversions')->sum(),
            'conversion_value' => $account_performance_reports->pluck('conversion_value')->sum(),
        ];
        unset($account->account_performance_report);
        $budget_commander = $account->budgetCommander()->first();
        if(is_null($budget_commander)){
            $account->rollover_spend = 0;
            $account->excess_budget = 0;
        }else{
            $account->rollover_spend = $budget_commander->select('rollover_spend')->first()->rollover_spend;
            $account->excess_budget = $budget_commander->select('excess_budget')->first()->excess_budget;
        }
            
        return $account;
    }

}
