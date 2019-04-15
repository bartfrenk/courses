use std::fs::File;
use std::io::prelude::*;


fn main() {
    let mut f = File::create("hello.txt").unwrap();
    f.write_all(b"Important message");
}
