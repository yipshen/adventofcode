fn main() {
    let mut data =
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
            });

    data.sort_by(|a, b| b.cmp(a));
    data.resize(3, 0);

    println!("{:?}", data.iter().sum::<i32>());
}
