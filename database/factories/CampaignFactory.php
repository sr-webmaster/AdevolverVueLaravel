<?php

use Illuminate\Support\Str;
use Faker\Generator as Faker;

$factory->define(App\Models\Campaign::class, function (Faker $faker) {
    return [
        'name' 		=> $faker->name.' campaign',
        'google_id' => Str::random(10),
    ];
});
