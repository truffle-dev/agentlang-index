```rust
use std::collections::HashMap;
use std::io::{self, Read, Write};

fn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    if n == 0 {
        return 0;
    }
    if n == 1 {
        return 1;
    }
    if let Some(&result) = memo.get(&n) {
        return result;
    }
    let result = fib(n - 1, memo) + fib(n - 2, memo);
    memo.insert(n, result);
    result
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: u64 = input.trim().parse().unwrap();
    
    let mut memo = HashMap::new();
    let result = fib(n, &mut memo);
    
    writeln!(io::stdout(), "{}", result).unwrap();
}
```