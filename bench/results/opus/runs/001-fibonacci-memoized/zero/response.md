```zero
const std = @import("std")

const main = fn(world: std.World) std.World {
  const n = check std.parse_int(world.args[1])
  const memo = std.mem.alloc(i64, n + 1)
  defer std.mem.free(memo)
  const result = fib(n, memo)
  const s = std.fmt.int_to_str(result)
  check world.out.write(s)
  check world.out.write("\n")
  return world
}

const fib = fn(n: i64, memo: std.mem.Span(i64)) i64 {
  if n == 0 {
    return 0
  }
  if n == 1 {
    return 1
  }
  if memo[n] != 0 {
    return memo[n]
  }
  const val = fib(n - 1, memo) + fib(n - 2, memo)
  memo[n] = val
  return val
}
```