
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}


struct Product {
    id: String,
    image_url: String,
}

fn main() {
    let s = String::from("hello, world!");

    let hello = &s[0..5];
    let world = &s[6..11];


}
