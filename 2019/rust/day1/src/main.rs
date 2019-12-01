
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

fn calc_fuel_amount(mass: i32) -> i32{
    let fuel;
    fuel = mass/3-2;
    fuel
}


fn calc_fuel_amount_recursive(mass: i32) -> i32{
    if mass <=5 {
        return 0;
    }
    let fuel;
    fuel = calc_fuel_amount(mass);
    return fuel + calc_fuel_amount_recursive(fuel);
}



fn main() {
    let input = load_from_file("input.txt");
    let mut fuel_amount = Vec::new();

    fuel_amount = input.iter().map(|x| calc_fuel_amount(*x)).collect();
    println!("Part 1: {}", fuel_amount.iter().sum::<i32>());

    fuel_amount = input.iter().map(|x| calc_fuel_amount_recursive(*x)).collect();
    println!("Part 2: {}",fuel_amount.iter().sum::<i32>());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calc_fuel_amount() {
        assert_eq!(2, calc_fuel_amount(12));
        assert_eq!(2, calc_fuel_amount(14));
        assert_eq!(654, calc_fuel_amount(1969));
        assert_eq!(33583, calc_fuel_amount(100756));
    }
     #[test]
    fn test_calc_fuel_amount_recursive() {
        assert_eq!(2, calc_fuel_amount_recursive(14));
        assert_eq!(966, calc_fuel_amount_recursive(1969));
        assert_eq!(50346, calc_fuel_amount_recursive(100756));
    }

}