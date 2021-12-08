use itertools::Itertools;
use std::fs;


fn sums_to_number(v: &[i32], n: i32, k: usize) -> Result<std::vec::Vec<&i32>, String> {
    for vpair in v.iter().combinations(k) {
        if vpair.clone().into_iter().sum::<i32>() == n {
            return Ok(vpair.to_owned());
        }
    }
    Err("No n entries sum to given value found".to_owned())
}

fn main() {
    let data = fs::read_to_string("input.txt").expect("Unable to read file");
    let vec: Vec<i32> = data.split("\n").map(|x| x.parse().unwrap()).collect();

    for n in 2..4 {
        println!("Running for {} entries", n);
        match sums_to_number(&vec, 2020, n) {
            Ok(res) => {
                println!(
                "{:?} sums to 2020, multiplied they are {}",
                res.clone(),
                res.into_iter().product::<i32>()
                )
            },
            Err(e) => println!("Error {:?}", e),
        }
    }
}

pub fn clone_vec<T: Clone>(vec: Vec<&T>) -> Vec<T> {
    vec.into_iter().cloned().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_day1() {
        let vec = vec![1721, 979, 366, 299, 675, 1456];
        if let Ok(res) = sums_to_number(&vec, 2020, 2) {
            assert_eq!(clone_vec(res), vec![1721, 299]);
        }
    }

    #[test]
    fn test_day1_fail() {
        let vec = vec![1, 2, 3];
        let result = sums_to_number(&vec, 10, 2);
        assert_eq!("No n entries sum to given value found", result.unwrap_err());
    }

    #[test]
    fn test_day2() {
        let vec = vec![1721, 979, 366, 299, 675, 1456];
        if let Ok(res) = sums_to_number(&vec, 2020, 3) {
            assert_eq!(clone_vec(res), vec![979, 366, 675]);
        }
    }
}
