extern crate array_tool;

use array_tool::vec::Intersect;
use itertools::Itertools;

fn main() {
    let alphabet: String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".to_string();

    println!(
        "{}",
        include_str!("../../../data/day03.txt")
            .lines()
            .chunks(3)
            .into_iter()
            .fold(0, |acc, mut chunk| {
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
