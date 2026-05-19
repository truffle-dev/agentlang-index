```zero
use std

fn main() -> Errors!Void
  let args = std.args()
  if args.len != 1
    check world.out.write("error\n")
    return

  let s = args[0]
  let n_s = s.len
  if n_s == 0
    check world.out.write("error\n")
    return

  // Parse non-negative integer from s (no leading '+' or '-' except optional '+')
  let i0 = 0
  let i = i0

  // Optional leading '+'
  if i < n_s
    let c0 = s[i]
    if c0 == 43
      // '+'
      let ni = i + 1
      if ni < n_s
        // Accept only if there's at least one digit after '+'
        // Update i to ni
        let i = ni
      else
        check world.out.write("error\n")
        return

  if i >= n_s
    check world.out.write("error\n")
    return

  // Ensure all remaining are digits and accumulate
  let any = false
  let n: u64 = 0
  let j = i
  let k = j
  while k < n_s
    let c = s[k]
    if c < 48
      check world.out.write("error\n")
      return
    let d = c - 48
    if d > 9
      check world.out.write("error\n")
      return
    // n = n * 10 + d
    let n10 = n * 10
    let n_new = n10 + (d as u64)
    let n = n_new
    let any = true
    let k = k + 1

  if not any
    check world.out.write("error\n")
    return

  // Compute fib(n) with iterative memoization (bottom-up)
  let a: u128 = 0
  let b: u128 = 1
  let cnt: u64 = n
  let aa = a
  let bb = b
  let c = 0u128
  let xcnt = cnt
  let a2 = aa
  let b2 = bb
  let t = c
  let i_cnt = xcnt
  let a3 = a2
  let b3 = b2
  while i_cnt > 0
    let t = a3 + b3
    let a3 = b3
    let b3 = t
    let i_cnt = i_cnt - 1

  let result = a3

  // Convert result to decimal and write
  if result == 0
    check world.out.write("0\n")
    return

  let buf: [64]u8
  let pos: u64 = 64
  let x = result
  let xx = x
  let p = pos
  let x_work = xx
  let p_work = p
  let ten = 10u128
  let zero_ch = 48u8
  let p_final = p_work
  let x_final = x_work
  let p_cur = p_final
  let x_cur = x_final
  while x_cur > 0
    let q = x_cur / ten
    let r = x_cur - q * ten
    let digit = (r as u8) + zero_ch
    let p_next = p_cur - 1
    buf[p_next] = digit
    let x_cur = q
    let p_cur = p_next

  check world.out.write(buf[p_cur..64])
  check world.out.write("\n")
  return
```