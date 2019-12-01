
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


fn main() {
    println!("{:?}", load_from_file("input.txt"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_() {
    }
}