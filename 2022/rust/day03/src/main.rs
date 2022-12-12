extern crate array_tool;

use array_tool::vec::Intersect;
use itertools::Itertools;

fn main() {
    let alphabet: String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".to_string();

    // Read the data.
    let rucksacks = include_str!("../../../data/day03.txt").lines();

    // Part 1.
    println!(
        "{}",
        rucksacks.clone().fold(0, |acc, line| {
            let chars = line.chars().collect::<Vec<char>>();

            let (left, right) = chars.split_at(chars.len() / 2);
            let c = left.to_vec().intersect(right.to_vec())[0];

            acc + alphabet.find(c).unwrap() + 1
        })
    );

    // Part 2.
    println!(
        "{}",
        rucksacks.chunks(3).into_iter().fold(0, |acc, mut chunk| {
            let (first, second, third) = (
                chunk.next().unwrap().chars().collect::<Vec<char>>(),
                chunk.next().unwrap().chars().collect::<Vec<char>>(),
                chunk.next().unwrap().chars().collect::<Vec<char>>(),
            );

            let c = first.intersect(second).intersect(third)[0];

            acc + alphabet.find(c).unwrap() + 1
        })
    );
}
