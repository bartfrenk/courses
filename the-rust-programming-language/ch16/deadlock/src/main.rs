use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn main() {
    let ma1 = Arc::new(Mutex::new(0));
    let mb1 = Arc::new(Mutex::new(0));

    let ma2 = Arc::clone(&ma1);
    let mb2 = Arc::clone(&mb1);

    let h1 = thread::spawn(move || {
        let a1 = ma1.lock().unwrap();
        thread::sleep(Duration::from_secs(1));
        println!("{:?}", a1);
        let b1 = mb1.lock().unwrap();
        println!("{:?}", b1);
    });

    let h2 = thread::spawn(move || {
        let b2 = mb2.lock().unwrap();
        thread::sleep(Duration::from_secs(1));
        println!("{:?}", b2);
        let a2 = ma2.lock().unwrap();
        println!("{:?}", a2);
    });

    h1.join().unwrap();
    h2.join().unwrap();
    println!("Never reached: deadlock!");
}
