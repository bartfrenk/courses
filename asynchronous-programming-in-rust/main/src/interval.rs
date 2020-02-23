use futures::stream::Stream;
use std::{
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
    thread,
    time::Duration,
};

pub struct IntervalTimer {
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
