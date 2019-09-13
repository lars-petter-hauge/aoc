
use std::io::prelude::*;
use std::path::Path;
use std::collections::HashMap;
extern crate itertools;
use itertools::Itertools;

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

fn similarity(xs: &String, ys: &String) -> String{
    let mut similarity = String::new();
    for (x, y) in xs.chars().zip(ys.chars()){
        if x == y {
            similarity.push(x)
        }
    }
    similarity.to_string()
}

fn check_similarity(vector: Vec<String>)-> String{
    let mut similar = String::new();
    let mut most_similar = String::new();
    for (a, b) in vector.iter().tuple_combinations(){
        similar = similarity(&a, &b);
        if similar.len() > most_similar.len(){
            most_similar = similar;
        }
    }
    most_similar.to_string()
}

fn main() {
    println!("{}", check_sum(load_from_file("input.txt")));
    println!("{}", check_similarity(load_from_file("input.txt")));
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

    #[test]
    fn test_similarity(){
        assert_eq!(similarity(&"equalweirdotheragain".to_string(),
                              &"equalsomethingeagain".to_string()),
                              "equalagain");
    }

    #[test]
    fn test_check_similarity(){
        assert_eq!(check_similarity(["abcde",
                                     "fghij",
                                     "klmno",
                                     "pqrst",
                                     "fguij",
                                     "axcye",
                                     "wvxyz"]
                                     .iter()
                                     .map(|&s| s.into())
                                     .collect()),
                                     "fgij");
    }
}