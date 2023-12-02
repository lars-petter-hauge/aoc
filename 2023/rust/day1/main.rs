use std::path::Path;

fn load_from_file(filename: impl AsRef<Path>) -> Vec<String> {
    let content = std::fs::read_to_string(filename).expect("unable to read file");
    let vec: Vec<String> = content.split("\n").map(|s: &str| s.to_string()).collect();
    vec
}

fn main() {
    use std::time::Instant;
    let now = Instant::now();
    let _lines = load_from_file("input.txt");
    //let numbers: Vec<Vec<u32>> = _lines
    //    .iter()
    //    .map(|line| line.chars().map(|c| c.to_digit(10)).collect())
    //    .collect();
    let mut numbers: Vec<u32> = vec![];
    let _iter = _lines.iter();
    for val in _iter {
        let char_iter = val.chars();
        let mut temp_num: Vec<u32> = vec![];
        for c in char_iter {
            let dig = c.to_digit(10);
            if !dig.is_none() {
                temp_num.push(dig.unwrap());
            }
        }

        if !temp_num.is_empty() {
            let val = format!(
                "{:?}{:?}",
                temp_num.first().unwrap(),
                temp_num.last().unwrap()
            );
            numbers.push(val.parse::<u32>().unwrap())
        }
    }
    println!("sum: {:?}", numbers.iter().sum::<u32>());
    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);
}

#[cfg(test)]
mod tests {
    use super::*;
}
