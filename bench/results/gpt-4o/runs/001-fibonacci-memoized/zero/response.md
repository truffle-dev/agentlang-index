```zero
use std

fn fib(n: u64, memo: &mut [u64]) -> u64 {
    if n < 2 {
        return n
    }
    if memo[n as usize] != 0 {
        return memo[n as usize]
    }
    memo[n as usize] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n as usize]
}

fn main() -> u8 {
    let args = std.args()
    if args.len() != 2 {
        check world.out.write("error\n")
        return 0
    }
    let n = std.parse_u64(args[1])
    if n.is_none() {
        check world.out.write("error\n")
        return 0
    }
    let n = n.unwrap()
    let mut memo = [0u64; 100] // assuming n <= 99 for simplicity
    let result = fib(n, &mut memo)
    let result_str = std.to_string(result)
    check world.out.write(result_str)
    check world.out.write("\n")
    return 0
}
```