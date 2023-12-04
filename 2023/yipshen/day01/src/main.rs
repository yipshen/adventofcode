fn compute_calibration_value(input: Vec<String>) -> u32 {
    let values = input
        .into_iter()
        .fold([].to_vec(), |mut values, line| {
            let digits = line
                .chars()
                .filter_map(|c| c.to_digit(10))
                .collect::<Vec<_>>();

            values.push(digits.first().unwrap() * 10 + digits.last().unwrap());
            values
        })
        .into_iter()
        .collect::<Vec<_>>();

    values.iter().sum::<u32>()
}

fn replace_digit(input: String) -> String {
    input
        .replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
}

fn main() {
    // Read the data.
    let lines = include_str!("../input.txt")
        .lines()
        .map(|line| line.to_string());

    // Part 1.
    let value = compute_calibration_value(lines.clone().into_iter().collect::<Vec<_>>());
    println!("{}", value);

    // Part 2.
    let value = compute_calibration_value(
        lines
            .map(replace_digit)
            .collect::<Vec<_>>()
            .into_iter()
            .collect::<Vec<_>>(),
    );
    println!("{}", value);
}
