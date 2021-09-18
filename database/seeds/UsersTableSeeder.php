<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UsersTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        factory(App\User::class)->create([
            'email'         => 'charlesbannister@gmail.com',
            'name'          => 'Charles Bannister',
            'password'      => Hash::make('password'),
            'admin'         =>  1,

            ]);

        factory(App\User::class)->create([
            'email'         => 'ed@adevolver.com',
            'name'          => 'Ed Leake',
            'password'      => Hash::make('password'),
            'admin'         =>  1,

            ]);

        factory(App\User::class)->create([
            'email'         => 'henrik@webtractive.com',
            'name'          => 'Henrik Nordstrom',
            'password'      => Hash::make('password'),
            'admin'         =>  1,

            ]);

        factory(App\User::class)->create([
            'email'         => 'lucasdanielotero1992@gmail.com',
            'name'          => 'Lucas Daniel Otero',
            'password'      => Hash::make('password'),
            'admin'         =>  1,

            ]);
    }
}
