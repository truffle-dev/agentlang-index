```zero
const N = check world.args[1].parseInt()
const memo = check world.alloc(8 * (N + 1))

let fib = fn(n: u64) -> u64 {
    if n == 0 {
        return 0
    }
    if n == 1 {
        return 1
    }
    if memo[n] != 0 {
        return memo[n]
    }
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]
}

let result = fib(N)
check world.out.write(result.toString().bytes())
check world.out.write("\n".bytes())
return
```