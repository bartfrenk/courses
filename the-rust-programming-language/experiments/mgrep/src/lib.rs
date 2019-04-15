use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

// TODO: Generalize `query` to arbitrary predicates.
// TODO: Write useful command line interface

pub fn run(path: &str, query: &str) -> Result<(), Box<dyn Error>> {
    let file = File::open(path)?;
    let results = BufReader::new(file)
        .lines()
        .map(|r| r.unwrap())
        .filter(|line| line.contains(query));

    for line in results {
        println!("{}", line);
    }
    Ok(())
}
