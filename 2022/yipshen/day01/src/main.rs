fn main() {
    // Read the data.
    let mut calories = include_str!("../input.txt")
        .lines()
        .fold([0].to_vec(), |mut data, line| {
            match line.parse::<i32>() {
                Ok(val) => {
                    if let Some(last) = data.last_mut() {
                        *last += val;
                    }
                }
                Err(_) => data.push(0),
            }
            data
        });

    // Part 1.
    println!("{}", calories.iter().max().unwrap());

    // Part 2.
    calories.sort_by(|a, b| b.cmp(a));
    calories.resize(3, 0);

    println!("{}", calories.iter().sum::<i32>());
}
