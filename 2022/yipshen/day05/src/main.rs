use std::{fs, str::FromStr};

#[derive(Debug)]
struct ActionError;

#[derive(Clone)]
struct Action {
    count: usize,
    src: usize,
    dst: usize,
}

impl FromStr for Action {
    type Err = ActionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let words: Vec<&str> = s.split(' ').collect();
        if words[0] != "move" || words[2] != "from" || words[4] != "to" {
            Err(Self::Err {})
        } else {
            Ok(Action {
                count: words[1].parse().unwrap(),
                src: words[3].parse().unwrap(),
                dst: words[5].parse().unwrap(),
            })
        }
    }
}

#[derive(Clone)]
struct CrateMover {
    stacks: Vec<String>,
    moves: Vec<Action>,
}

impl CrateMover {
    pub fn from_file(input: &str) -> Self {
        // Read the data.
        let file_content = fs::read_to_string(input).unwrap();
        let lines = file_content.lines();

        // Build the starting stacks.
        let index = lines
            .clone()
            .enumerate()
            .find(|line| line.1.to_string().starts_with(" 1 "))
            .unwrap()
            .0;

        let count = (lines.clone().nth(index).unwrap().len() + 1) / 4;

        let stacks = lines
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

        let moves = lines
            .clone()
            .skip(count + 1)
            .map(|line| Action::from_str(line).unwrap())
            .collect::<Vec<_>>();

        Self { stacks, moves }
    }

    fn move_crates(mut self, reverse_move: bool) -> String {
        self.moves.iter().for_each(|action| {
            let mut s = self.stacks[action.src - 1]
                .chars()
                .rev()
                .take(action.count)
                .collect::<String>();
            if !reverse_move {
                s = s.chars().rev().collect::<String>();
            }

            self.stacks[action.dst - 1].push_str(s.as_str());

            let new_len = self.stacks[action.src - 1].len() - action.count;
            self.stacks[action.src - 1].truncate(new_len);
        });

        self.stacks.iter().fold("".to_owned(), |acc, stack| {
            let mut str = acc;
            str.push_str(&format!("{}", stack.chars().last().unwrap()));
            str
        })
    }

    pub fn move_9000(self) -> String {
        self.move_crates(true)
    }

    pub fn move_9001(self) -> String {
        self.move_crates(false)
    }
}

fn main() {
    let mover = CrateMover::from_file("input.txt");

    // Part 1.
    println!("{}", mover.clone().move_9000());

    // Part 2.
    println!("{}", mover.move_9001());
}
