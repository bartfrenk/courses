use std::fs::File;
use std::io::{BufRead, BufReader, Result};

fn main() {
    print_file_by_line("Cargo.toml").unwrap();

    let v1: Vec<i32> = vec![1, 2, 3];

    let v2: Vec<_> = v1.iter().map(|x| x + 1).collect();

    println!("{:?}", v2);
}

fn print_file_by_line(path: &str) -> Result<()> {
    let file = File::open(path)?;
    for line in BufReader::new(file).lines() {
        println!("{}", line?);
    }
    Ok(())
}
