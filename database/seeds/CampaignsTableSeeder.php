<?php

use App\Models\Account;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class CampaignsTableSeeder extends Seeder
{
    public function run()
    {
        foreach (Account::all() as $account) {
            factory(App\Models\Campaign::class, 2)->create([
                'account_id'	=>	$account->id,
            ]);
        }
    }
}
