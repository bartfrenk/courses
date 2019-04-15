mod lib;
use lib::run;

fn main() {
    run("res/multi.txt", "tell").unwrap();
}
