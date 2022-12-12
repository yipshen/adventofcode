use std::collections::HashSet;

fn find_marker(message: &str, count: usize) -> usize {
    let mut marker = "".to_string();
    for candidate in message.chars().collect::<Vec<_>>().windows(count) {
        let mut chars = HashSet::new();
        for c in candidate {
            chars.insert(c);
        }
        if chars.len() == count {
            marker = candidate.iter().collect::<String>();
            break;
        }
    }
    message.find(marker.as_str()).unwrap() + count
}

fn main() {
    // Read the data.
    let message = include_str!("../input.txt").lines().next().unwrap();

    // Part 1.
    println!("{}", find_marker(message, 4));

    // Part 2.
    println!("{}", find_marker(message, 14));
}
