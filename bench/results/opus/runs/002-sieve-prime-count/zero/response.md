```zero
fn main() -> u8
  let args = std.args()
  if args.len() < 2
    check world.out.write("0\n")
    return 0
  let n_str = args[1]
  let n = parse_int(n_str)
  if n < 2
    check world.out.write("0\n")
    return 0
  let size = n + 1
  mut sieve: [10001]bool = undefined
  mut i: u32 = 0
  loop
    if i >= size
      break
    sieve[i] = true
    i = i + 1
  sieve[0] = false
  sieve[1] = false
  mut p: u32 = 2
  loop
    if p * p > n
      break
    if sieve[p]
      mut m: u32 = p * p
      loop
        if m >= size
          break
        sieve[m] = false
        m = m + p
    p = p + 1
  mut count: u32 = 0
  mut j: u32 = 2
  loop
    if j >= size
      break
    if sieve[j]
      count = count + 1
    j = j + 1
  mut buf: [20]u8 = undefined
  let len = int_to_str(count, buf)
  check world.out.write(buf[0..len])
  check world.out.write("\n")
  return 0

fn parse_int(s: []u8) -> u32
  mut result: u32 = 0
  mut idx: u32 = 0
  loop
    if idx >= s.len()
      break
    let c = s[idx]
    if c < 48
      break
    if c > 57
      break
    result = result * 10 + (c - 48)
    idx = idx + 1
  return result

fn int_to_str(val: u32, mut buf: [20]u8) -> u32
  if val == 0
    buf[0] = 48
    return 1
  mut n = val
  mut len: u32 = 0
  loop
    if n == 0
      break
    let digit = n % 10
    buf[len] = @as(u8, digit + 48)
    len = len + 1
    n = n / 10
  mut left: u32 = 0
  mut right: u32 = len - 1
  loop
    if left >= right
      break
    let tmp = buf[left]
    buf[left] = buf[right]
    buf[right] = tmp
    left = left + 1
    right = right - 1
  return len
```