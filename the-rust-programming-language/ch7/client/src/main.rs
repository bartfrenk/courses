extern crate communicator;

fn main() {
    let red = Red;
    let yellow = Yellow;
    communicator::client::connect();
}

pub enum TrafficLight {
    Red,
    Yellow,
    Green,
}

use TrafficLight::{Red, Yellow};
