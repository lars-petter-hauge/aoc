
use std::io::prelude::*;
use std::path::Path;
use std::collections::HashMap;

fn load_from_file(filename: impl AsRef<Path>)-> Vec<String>
{
    let file = std::fs::File::open(filename).expect("could not open line");
    let buf = std::io::BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("could not parse line"))
        .collect()
}

fn check_sum(vector: Vec<String>)-> i32{
    let mut thrice = 0;
    let mut twice = 0;
    let mut frequency: HashMap<char, u32> = HashMap::new();

    for check_str in vector{
        frequency.clear();
        for character in check_str.chars() {
            *frequency.entry(character).or_insert(0) += 1;
        }
        if frequency.values().any(|&x| x==2){
            twice += 1
        }
        if frequency.values().any(|&x| x==3){
            thrice += 1
        }
    }
    twice * thrice
}

fn main() {
    println!("{}", check_sum(load_from_file("input.txt")));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_checksum() {
        assert_eq!(check_sum(["abcdef",
                              "bababc",
                              "abbcde",
                              "abcccd",
                              "aabcdd",
                              "abcdee",
                              "ababab"]
                             .iter()
                             .map(|&s| s.into())
                             .collect()), 
                             12);
    }
}