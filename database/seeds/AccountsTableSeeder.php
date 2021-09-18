<?php

use App\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class AccountsTableSeeder extends Seeder
{
    public function run()
    {
        foreach (User::all() as $user) {
            factory(App\Models\Account::class, 1200)->create([
                'user_id'	=>	$user->id,
                'google_id'	=> 'test',
            ]);
        }
    }
}
