<?php
$input = trim(file_get_contents(__DIR__ . '/input/day03.txt'));

// Priority table
$p = str_split('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ');
$p = array_combine(array_values($p), array_keys($p));

// Part 1
$r = array_map(function ($v) use ($p) {
	$v = trim($v);
	$b = str_split($v, strlen($v) / 2);
	$r = array_unique(array_intersect(str_split($b[0]), str_split($b[1])));
	$priority = 0;
	foreach ($r as $type) {
		$priority += $p[$type] + 1;
	}
	return $priority;
}, explode("\n", trim($input)));

var_dump(array_sum($r));

// Part 2
$r = array_map(function ($b) use ($p) {
	$r = array_values(array_unique(array_intersect(str_split(trim($b[0])), str_split(trim($b[1])), str_split(trim($b[2])))));
	$priority = 0;
	if (isset($r[0])) {
		$priority = $p[$r[0]] + 1;
	}
	return $priority;
}, array_chunk(explode("\n", trim($input)), 3));

var_dump(array_sum($r));