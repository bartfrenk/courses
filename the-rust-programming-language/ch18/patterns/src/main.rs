fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Yeah!")
    }
}

fn test(Some(x): Option<u32>) {
    println!("{}", x);
}
