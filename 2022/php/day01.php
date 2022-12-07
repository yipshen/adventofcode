<?php

$input = file_get_contents(__DIR__ . '/../data/day01.txt');

$a = array_map(fn($v) => array_sum(explode("\n", $v)), explode("\n\n", $input));

var_dump(max($a));

arsort($a);

$b = array_values($a);

var_dump($b[0] + $b[1] + $b[2]);