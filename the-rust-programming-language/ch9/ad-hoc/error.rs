use std::fmt::Debug;

#[derive(Debug)]
struct CustomErr {
    value: i32,
}

fn make(_i: i32) -> Result<i32, i32> {
    return Err(1);
}

impl From<i32> for CustomErr {
    fn from(i: i32) -> Self {
        return CustomErr { value: i };
    }
}

fn wrap() -> Result<i32, CustomErr> {
    return make(make(0)?).map_err(|error| CustomErr { value: error });
}

fn largest<T: PartialOrd>(xs: &[T]) -> &T {
    let &largest = xs[0];
    for &item in xs.iter() {
        if item > largest {
            largest = item;
        }
    }
    return largest;
}



fn debug<T>(i: T)
where
    T: Debug,
{
    println!("{:?}\n", i)
}

fn main() {
    debug(wrap());
}
