#[derive(Debug)]
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

fn build_user(email: &str, username: &str) -> User {
    User {
        email: String::from(email),
        username: String::from(username),
        active: true,
        sign_in_count: 1,
    }
}

struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let x = Some(5);

    let mut user = build_user("bart.frenk@gmail.com", "bart");
    user.active = false;
    println!("Created user {user:?}", user = user);

    let rect = Rectangle {
        width: 30,
        height: 50,
    };

    println!("The area of the rectangle is {}", rect.area());
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
