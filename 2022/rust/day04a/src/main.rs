use std::str::FromStr;

struct Interval(i32, i32);

impl Interval {
    pub fn contains(&self, other: &Self) -> bool {
        self.0 <= other.0 && self.1 >= other.1
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
    println!(
        "{}",
        include_str!("../../../data/day04.txt")
            .lines()
            .fold(0, |acc, line| {
                let intervals = line.split(',').collect::<Vec<&str>>();

                let first = Interval::from_str(intervals[0]).unwrap();
                let second = Interval::from_str(intervals[1]).unwrap();

                if first.contains(&second) || second.contains(&first) {
                    acc + 1
                } else {
                    acc
                }
            })
    );
}
