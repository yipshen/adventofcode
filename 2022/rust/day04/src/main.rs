use std::str::FromStr;

struct Interval(i32, i32);

impl Interval {
    pub fn contains(&self, other: &Self) -> bool {
        self.0 <= other.0 && self.1 >= other.1
    }

    pub fn overlaps(&self, other: &Self) -> bool {
        self.0 <= other.0 && self.1 >= other.0
            || self.0 <= other.1 && self.1 >= other.1
            || self.0 <= other.0 && self.1 >= other.1
    }
}

impl FromStr for Interval {
    type Err = IntervalError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let p = s.split('-').collect::<Vec<&str>>();
        Ok(Interval(p[0].parse().unwrap(), p[1].parse().unwrap()))
    }
}

#[derive(Debug)]
struct IntervalError;

fn main() {
    // Read the data.
    let intervals = include_str!("../../../data/day04.txt").lines();

    // Compute counts.
    let (contains_count, overlaps_count) = intervals.clone().fold((0, 0), |acc, line| {
        let intervals = line.split(',').collect::<Vec<&str>>();

        let first = Interval::from_str(intervals[0]).unwrap();
        let second = Interval::from_str(intervals[1]).unwrap();

        let mut contains_inc = 0;
        if first.contains(&second) || second.contains(&first) {
            contains_inc = 1;
        }

        let mut overlaps_inc = 0;
        if first.overlaps(&second) || second.overlaps(&first) {
            overlaps_inc = 1;
        }

        (acc.0 + contains_inc, acc.1 + overlaps_inc)
    });

    // Part 1.
    println!("{}", contains_count);

    // Part 2.
    println!("{}", overlaps_count);
}
