use futures::{
    future::{Fuse, FusedFuture, FutureExt},
    pin_mut, select,
    stream::{FusedStream, FuturesUnordered, Stream, StreamExt},
};
use std::{
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
    thread,
    time::Duration,
};

async fn get_new_num() -> u8 {
    5
}

async fn run_on_new_num(i: u8) -> u8 {
    println!("Processing {}", i);
    i
}

async fn run_loop(
    mut interval_timer: impl Stream<Item = ()> + FusedStream + Unpin,
    starting_num: u8,
) {
    let mut run_on_new_num_futs = FuturesUnordered::new();
    run_on_new_num_futs.push(run_on_new_num(starting_num));
    let get_new_num_fut = Fuse::terminated();
    pin_mut!(get_new_num_fut);
    loop {
        select! {
            () = interval_timer.select_next_some() => {
                if get_new_num_fut.is_terminated() {
                    get_new_num_fut.set(get_new_num().fuse());
                }
            },
            new_num = get_new_num_fut => {
                run_on_new_num_futs.push(run_on_new_num(new_num));
            },
            res = run_on_new_num_futs.select_next_some() => {
                println!("run_on_new_num_fut returned {:?}", res);
            },
            complete => panic!("`interval_timer` completed unexpectedly")
        }
    }
}

#[tokio::main]
async fn main() {
    let timer = IntervalTimer::new(Duration::from_millis(100)).fuse();
    run_loop(timer, 8).await;
    println!("Hello, world!");
}

struct IntervalTimer {
    shared_state: Arc<Mutex<SharedState>>,
}

struct SharedState {
    waker: Option<Waker>,
    completed: bool,
}

impl Stream for IntervalTimer {
    type Item = ();
    fn poll_next(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Option<Self::Item>> {
        let mut shared_state = self.shared_state.lock().unwrap();
        if shared_state.completed {
            shared_state.completed = false;
            // TODO: What is the difference between returning Some(()) and None?
            Poll::Ready(Some(()))
        } else {
            // TODO: Reread the part about needing to clone the waker
            shared_state.waker = Some(cx.waker().clone());
            Poll::Pending
        }
    }
}

impl IntervalTimer {
    pub fn new(duration: Duration) -> Self {
        let shared_state = Arc::new(Mutex::new(SharedState {
            completed: false,
            waker: None,
        }));

        // This clones the reference, not the referent
        let thread_shared_state = shared_state.clone();
        thread::spawn(move || loop {
            thread::sleep(duration);
            let mut shared_state = thread_shared_state.lock().unwrap();
            shared_state.completed = true;
            if let Some(waker) = shared_state.waker.take() {
                waker.wake()
            }
        });

        IntervalTimer { shared_state }
    }
}
