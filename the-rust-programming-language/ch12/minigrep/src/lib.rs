use std::env;
use std::error::Error;
use std::fs::File;
use std::io;
use std::io::{BufRead, BufReader};

// // TODO: Run this in constant memory (do not load complete file)

// // #[cfg(test)]
// // mod tests {
// //     use super::*;

// //     #[test]
// //     fn one_result() {
// //         let query = "duct";
// //         let contents = "\
// // Rust:
// // safe, fast, productive.
// // Pick three.
// // Duct tape.";

// //         assert_eq!(vec!["safe, fast, productive."], search(query, contents));
// //     }

// //     #[test]
// //     fn case_insensitive() {
// //         let query = "rUsT";
// //         let contents = "\
// // Rust:
// // safe, fast, productive.
// // Pick three.
// // Trust me.";
// //         assert_eq!(
// //             vec!["Rust:", "Trust me."],
// //             search_case_insensitive(query, contents)
// //         );
// //     }
// // }

// fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
//     let query = query.to_lowercase();
//     let mut results = Vec::new();

//     for line in contents.lines() {
//         if line.to_lowercase().contains(&query) {
//             results.push(line);
//         }
//     }

//     results
// }

// fn search<'a, I>(query: &str, contents: I) -> Iterator<Item = String>
// where
//     I: Iterator<Item = io::Result<String>>,
// {
//     contents.filter(|maybeLine| match maybeLine {
//         Err(_) => false,
//         Ok(line) => line.contains(query),
//     })
// }

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let file = File::open(config.filename)?;
    let results = BufReader::new(file).lines().map(|r| r.unwrap());
    //        .filter(|line| line.contains(config.query));

    //     .filter(|res| match res {
    //     Err(_) => false,
    //     Ok(line) => line.contains(config.query),
    // });

    // } else {
    //     search_case_insensitive(&config.query, &contents)
    // };

    for line in results {
        println!("{}", line);
    }
    Ok(())
}

pub struct Config {
    pub query: String,
    pub filename: String,
    pub case_sensitive: bool,
}

impl Config {
    pub fn new(mut args: env::Args) -> Result<Config, &'static str> {
        args.next();

        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = match args.next() {
            Some(arg) => arg,
            None => return Err("No query string"),
        };

        let filename = match args.next() {
            Some(arg) => arg,
            None => return Err("No file name"),
        };

        let case_sensitive = env::var("CASE_INSENSITIVE").is_err();

        Ok(Config {
            query,
            filename,
            case_sensitive,
        })
    }
}
