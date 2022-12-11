extern crate array_tool;

use array_tool::vec::Intersect;

fn main() {
    let alphabet: String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".to_string();

    println!(
        "{}",
        include_str!("../../../data/day03.txt")
            .lines()
            .fold(0, |acc, line| {
                let chars = line.chars().collect::<Vec<char>>();

                let (left, right) = chars.split_at(chars.len() / 2);
                let c = left.to_vec().intersect(right.to_vec())[0];

                acc + alphabet.find(c).unwrap() + 1
            })
    );
}
