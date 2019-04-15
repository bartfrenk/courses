
fn main() {
    let s = String::from("hello");
    let x = 5;

    println!("{}, {}", s, x);

    takes_ownership(s);
    makes_copy(x);

    println!("{}, {}", s, x);
}


fn takes_ownership(some_string: String) {
    println!("{}", some_string);
}

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
}
