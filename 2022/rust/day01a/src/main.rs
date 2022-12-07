fn main() {
    println!(
        "{}",
        include_str!("../../../data/day01.txt")
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
            })
            .iter()
            .max()
            .unwrap()
    );
}
