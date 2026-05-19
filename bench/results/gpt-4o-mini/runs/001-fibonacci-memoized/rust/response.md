```rust
use std::io::{self, Read, Write};
use std::collections::HashMap;

fn fib(n: u64, memo: &mut HashMap<u64, u64>) -> u64 {
    if let Some(&result) = memo.get(&n) {
        return result;
    }
    let result = match n {
        0 => 0,
        1 => 1,
        _ => fib(n - 1, memo) + fib(n - 2, memo),
    };
    memo.insert(n, result);
    result
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let n: u64 = input.trim().parse().unwrap();
    
    let mut memo = HashMap::new();
    let result = fib(n, &mut memo);
    
    let mut output = String::new();
    output.push_str(&result.to_string());
    output.push('\n');
    
    io::stdout().write_all(output.as_bytes()).unwrap();
}
```