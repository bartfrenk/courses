use std::io;

fn takes_ownership(some_string: String) -> String {
    println!("{}", some_string);
    return some_string;
}

fn main() {
    let mut s1 = String::from("hello");
    s1 = takes_ownership(s1);

    println!("{}, world!", s1);

}
