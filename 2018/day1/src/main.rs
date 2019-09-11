
use std::io::prelude::*;
use std::path::Path;

fn load_from_file(filename: impl AsRef<Path>)-> Vec<i32>
{
    let file = std::fs::File::open(filename).expect("could not open line");
    let buf = std::io::BufReader::new(file);
    let mut vec: Vec<String> = buf.lines()
                                    .map(|l| l.expect("could not parse line"))
                                    .collect();

    vec.into_iter()
        .map(|x| x.parse::<i32>().unwrap())
        .collect()
}

fn running_total(frequencies: Vec<i32>)-> i32{
    let mut sum = 0;
    for freq in frequencies{
        sum += freq
    }
    sum
}

fn main() {
    println!("{}",running_total(load_from_file("input.txt")));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_running_total() {
        assert_eq!(running_total(vec![1, -2, 3, 1]), 3);
        assert_eq!(running_total(vec![1, 1, 1]), 3);
        assert_eq!(running_total(vec![1, 1, -2]), 0);
        assert_eq!(running_total(vec![-1, -2, -3]), -6);
    }
}