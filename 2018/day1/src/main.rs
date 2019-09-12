
use std::io::prelude::*;
use std::path::Path;

fn load_from_file(filename: impl AsRef<Path>)-> Vec<i32>
{
    let file = std::fs::File::open(filename).expect("could not open line");
    let buf = std::io::BufReader::new(file);
    let vec: Vec<String> = buf.lines()
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

fn frequency_seen_twice(frequencies: Vec<i32>)-> i32{
    let mut sum = 0;
    let mut i = 0;
    let mut running = Vec::new();
    loop{
        if i == frequencies.len(){
            i = 0;
        }
        sum += frequencies[i];
        if running.contains(&sum){
            break;
        }
        running.push(sum);
        i += 1;
    }
    sum
}


fn main() {
    println!("{}",running_total(load_from_file("input.txt")));
    println!("{}", frequency_seen_twice(load_from_file("input.txt")))
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

    #[test]
    fn test_frequency_twice() {
        assert_eq!(frequency_seen_twice(vec![7, 7, -2, -7, -4]), 14);
        assert_eq!(frequency_seen_twice(vec![-6, 3, 8, 5, -6]), 5);
        assert_eq!(frequency_seen_twice(vec![3, 3, 4, -2, -4]), 10);
        assert_eq!(frequency_seen_twice(vec![1, -1]), 0);
    }
}