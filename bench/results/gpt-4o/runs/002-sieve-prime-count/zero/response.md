```zero
use std

fn sieve_of_eratosthenes(n: u32) -> u32 {
    if n < 2 {
        return 0
    }
    
    let mut is_prime = std.vec<bool>(n + 1, true)
    is_prime[0] = false
    is_prime[1] = false
    
    let mut p = 2
    while p * p <= n {
        if is_prime[p] {
            let mut multiple = p * p
            while multiple <= n {
                is_prime[multiple] = false
                multiple += p
            }
        }
        p += 1
    }
    
    let mut count = 0
    for i in 2..=n {
        if is_prime[i] {
            count += 1
        }
    }
    
    return count
}

fn main() {
    let args = std.args()
    if args.len() != 2 {
        check world.out.write("error\n")
        return
    }
    
    let n = std.parse_u32(args[1])
    match n {
        Some(value) => {
            let count = sieve_of_eratosthenes(value)
            check world.out.write(std.fmt("{}\n", count))
        }
        None => {
            check world.out.write("error\n")
        }
    }
    
    return
}
```