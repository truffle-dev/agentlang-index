// Fibonacci with memoization, Rust reference.
// Reads N from stdin, caches fib(i) in a HashMap<u32, u64>.
// u64 holds fib(N) for N up to 93 (fib(93) = 12200160415121876738).
use std::collections::HashMap;
use std::io::{self, Read, Write};

fn fib(k: u32, memo: &mut HashMap<u32, u64>) -> u64 {
    if let Some(&v) = memo.get(&k) {
        return v;
    }
    let v = fib(k - 1, memo) + fib(k - 2, memo);
    memo.insert(k, v);
    v
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("read stdin");
    let n: u32 = input
        .trim()
        .parse()
        .expect("N must be a non-negative integer");
    let mut memo: HashMap<u32, u64> = HashMap::new();
    memo.insert(0, 0);
    memo.insert(1, 1);
    let v = fib(n, &mut memo);
    let stdout = io::stdout();
    let mut out = stdout.lock();
    write!(out, "{}\n", v).expect("write stdout");
}
