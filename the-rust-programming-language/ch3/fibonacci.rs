use std::io;

fn read_u32() -> u32 {
    println!("Please type a number");

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect(
        "Failed to read line",
    );

    return input.trim().parse().expect("Not a number");
}

fn fibonacci(n: u32) -> u64 {
    let mut m = n;
    let mut t: (u64, u64) = (0, 1);
    while m > 0 {
        t = (t.1, t.0 + t.1);
        m = m - 1;
    }
    return t.0;
}


fn main() {
    let m = read_u32();

    for n in 1..(m + 1) {
        println!("{}: {}", n, fibonacci(n))
    }
}
