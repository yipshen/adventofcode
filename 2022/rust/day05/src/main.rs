use core::str;
use std::str::FromStr;

struct MoveAction {
    count: i32,
    src: i32,
    dst: i32,
}

#[derive(Debug)]
struct MoveActionError;

impl FromStr for MoveAction {
    type Err = MoveActionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let words: Vec<&str> = s.split(' ').collect();
        if words[0] != "move" || words[2] != "from" || words[4] != "to" {
            Err(Self::Err {})
        } else {
            Ok(MoveAction {
                count: words[1].parse().unwrap(),
                src: words[3].parse().unwrap(),
                dst: words[5].parse().unwrap(),
            })
        }
    }
}

fn main() {
    // Read the data.
    let lines = include_str!("../../../data/day05.txt").lines();

    // Build the starting stacks.
    let index = lines
        .clone()
        .enumerate()
        .find(|line| line.1.to_string().starts_with(" 1 "))
        .unwrap()
        .0;

    let count = (lines.clone().nth(index).unwrap().len() + 1) / 4;

    let mut stacks = lines
        .clone()
        .take(index)
        .collect::<Vec<&str>>()
        .iter()
        .rev()
        .fold(vec!["".to_string(); count], |mut stacks, line| {
            for (i, c) in line.chars().enumerate() {
                if c.is_ascii_uppercase() {
                    stacks[(i - 1) / 4].push_str(&format!("{}", c));
                }
            }
            stacks
        });

    lines.skip(count + 1).for_each(|line| {
        let move_action = MoveAction::from_str(line).unwrap();
        // TODO: do the move.
    });

    println!(
        "{}",
        stacks.iter().fold("".to_owned(), |acc, stack| {
            let mut str = acc;
            str.push_str(&format!("{}", stack.chars().last().unwrap()));
            str
        })
    );
}
