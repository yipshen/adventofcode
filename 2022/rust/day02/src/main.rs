use std::str::FromStr;

#[derive(PartialEq, Eq)]
enum Sign {
    Rock,
    Paper,
    Scissors,
}

enum BattleOutcome {
    Win,
    Loss,
    Draw,
}

fn battle(me: Sign, other: Sign) -> BattleOutcome {
    if me == other {
        BattleOutcome::Draw
    } else if me == Sign::Rock && other == Sign::Scissors
        || me == Sign::Paper && other == Sign::Rock
        || me == Sign::Scissors && other == Sign::Paper
    {
        BattleOutcome::Win
    } else {
        BattleOutcome::Loss
    }
}

fn sign(me: Sign, other: Sign) -> Sign {
    if me == Sign::Paper {
        other
    } else if me == Sign::Rock {
        if other == Sign::Rock {
            Sign::Scissors
        } else if other == Sign::Paper {
            Sign::Rock
        } else {
            Sign::Paper
        }
    } else {
        if other == Sign::Rock {
            Sign::Paper
        } else if other == Sign::Paper {
            Sign::Scissors
        } else {
            Sign::Rock
        }
    }
}

#[derive(Debug)]
struct SignError;

impl FromStr for Sign {
    type Err = SignError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.eq("A") || s.eq("X") {
            Ok(Sign::Rock)
        } else if s.eq("B") || s.eq("Y") {
            Ok(Self::Paper)
        } else if s.eq("C") || s.eq("Z") {
            Ok(Self::Scissors)
        } else {
            Err(SignError {})
        }
    }
}

fn main() {
    // Read the data.
    let strategy = include_str!("../../../data/day02.txt")
        .lines()
        .map(|line| line.split(' ').collect::<Vec<&str>>());

    // Part 1.
    println!(
        "{}",
        strategy.clone().fold(0, |acc, values| {
            let left = Sign::from_str(values[0]).unwrap();
            let right = Sign::from_str(values[1]).unwrap();

            let sign_score = match right {
                Sign::Rock => 1,
                Sign::Paper => 2,
                Sign::Scissors => 3,
            };

            let battle_score = match battle(right, left) {
                BattleOutcome::Win => 6,
                BattleOutcome::Loss => 0,
                BattleOutcome::Draw => 3,
            };

            acc + battle_score + sign_score
        })
    );

    // Part 2.
    println!(
        "{}",
        strategy.fold(0, |acc, values| {
            let left = Sign::from_str(values[0]).unwrap();
            let right = Sign::from_str(values[1]).unwrap();

            let battle_score = match right {
                Sign::Scissors => 6,
                Sign::Rock => 0,
                Sign::Paper => 3,
            };

            let sign_score = match sign(right, left) {
                Sign::Rock => 1,
                Sign::Paper => 2,
                Sign::Scissors => 3,
            };

            acc + battle_score + sign_score
        })
    );
}
