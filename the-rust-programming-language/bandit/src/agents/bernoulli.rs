use std::collections::HashMap;

struct Beta {
    alpha: u32,
    beta: u32
};

struct GreedyBandit {
    prior: HashMap<String, Beta>
}
