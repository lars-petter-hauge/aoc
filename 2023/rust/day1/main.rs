use std::path::Path;

fn load_from_file(filename: impl AsRef<Path>) -> String {
    let content = std::fs::read_to_string(filename).expect("unable to read file");
    content
}

fn main() {
    use std::time::Instant;
    let now = Instant::now();
    let _lines = load_from_file("input.txt");
    //let numbers: Vec<Vec<u32>> = _lines
    //    .iter()
    //    .map(|line| line.chars().map(|c| c.to_digit(10)).collect())
    //    .collect();
    let mut numbers= Vec::new();
    for line in _lines.lines() {
        let mut temp_num= Vec::new();
        for c in line.chars() {
            if c.is_numeric(){
                temp_num.push(c);
            }
        }
        numbers.push((temp_num.first().unwrap().to_string()+&temp_num.last().unwrap().to_string()).parse::<i32>().unwrap())
    }
    println!("sum: {:?}", numbers.iter().sum::<i32>());
    let elapsed = now.elapsed();
    println!("Elapsed: {:.2?}", elapsed);
}

#[cfg(test)]
mod tests {
    use super::*;
}
