<?php
$input = file_get_contents(__DIR__ . '/input/day02.txt');

/**
 * A = rock
 * B = paper
 * C = scissor
 *
 * X = rock     1
 * Y = paper    2
 * Z = scissor  3
 *
 * A X = rock rock       3 + 1 = 4
 * A Y = rock paper      6 + 2 = 8
 * A Z = rock scissor    0 + 3 = 3
 *
 * B X = paper rock      0 + 1 = 1
 * B Y = paper paper     3 + 2 = 5
 * B Z = paper scissor   6 + 3 = 9
 *
 * C X = scissor rock    6 + 1 = 7
 * C Y = scissor paper   0 + 2 = 2
 * C Z = scissor scissor 3 + 3 = 6
 */
$r = [
	'A X' => 4,
	'A Y' => 8,
	'A Z' => 3,
	'B X' => 1,
	'B Y' => 5,
	'B Z' => 9,
	'C X' => 7,
	'C Y' => 2,
	'C Z' => 6,
];
$a = array_sum(array_map(fn($v) => $r[$v], explode("\n", trim($input))));
var_dump($a);

/**
 * A = rock
 * B = paper
 * C = scissor
 *
 * X = lose
 * Y = draw
 * Z = win
 *
 * A X = rock scissor    0 + 3 = 3
 * A Y = rock rock       3 + 1 = 4
 * A Z = rock paper      6 + 2 = 8
 *
 * B X = paper rock      0 + 1 = 1
 * B Y = paper paper     3 + 2 = 5
 * B Z = paper scissor   6 + 3 = 9
 *
 * C X = scissor paper   0 + 2 = 2
 * C Y = scissor scissor 3 + 3 = 6
 * C Z = scissor rock    6 + 1 = 7
 */
$r = [
	'A X' => 3,
	'A Y' => 4,
	'A Z' => 8,
	'B X' => 1,
	'B Y' => 5,
	'B Z' => 9,
	'C X' => 2,
	'C Y' => 6,
	'C Z' => 7,
];
$a = array_sum(array_map(fn($v) => $r[$v], explode("\n", trim($input))));
var_dump($a);