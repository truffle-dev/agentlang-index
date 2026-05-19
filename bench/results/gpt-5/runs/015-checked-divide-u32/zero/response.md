```zero
use std.args

fn is_ws(b: u8) -> bool {
  return b == 32 || b == 9 || b == 10 || b == 13
}

fn trim_trailing_ws(s: Span<u8>) -> Span<u8> {
  let mut n = s.len()
  while n > 0 {
    let c = s[n - 1]
    if !is_ws(c) {
      break
    }
    n = n - 1
  }
  return s[0..n]
}

fn parse_u32_trim_trailing(s: Span<u8>, out: *u32) -> bool {
  let t = trim_trailing_ws(s)
  let n = t.len()
  if n == 0 {
    return false
  }
  let mut val: u32 = 0
  let mut i: usize = 0
  let max_div10: u32 = 429496729
  let max_mod10: u32 = 5
  while i < n {
    let c = t[i]
    if c < 48 || c > 57 {
      return false
    }
    let digit: u32 = (c - 48) as u32
    if val > max_div10 {
      return false
    }
    if val == max_div10 && digit > max_mod10 {
      return false
    }
    val = val * 10 + digit
    i = i + 1
  }
  *out = val
  return true
}

fn write_error() -> Result<void> {
  check world.out.write("error\n")
  return Ok(void)
}

fn write_u32_line(x: u32) -> Result<void> {
  // Max 10 digits + '\n'
  let mut buf: [11]u8
  let mut n: usize = 0
  if x == 0 {
    buf[0] = 48
    n = 1
  } else {
    let mut v = x
    while v > 0 {
      let d = (v % 10) as u8
      buf[n] = 48 + d
      n = n + 1
      v = v / 10
    }
    // reverse first n bytes
    let mut i: usize = 0
    while i < n / 2 {
      let tmp = buf[i]
      buf[i] = buf[n - 1 - i]
      buf[n - 1 - i] = tmp
      i = i + 1
    }
  }
  buf[n] = 10
  n = n + 1
  check world.out.write(buf[0..n])
  return Ok(void)
}

fn main() -> Result<void> {
  let argv = args.all()
  if argv.len() < 3 {
    check write_error()
    return Ok(void)
  }
  let a_s = argv[1]
  let b_s = argv[2]

  let mut a: u32 = 0
  let mut b: u32 = 0

  if !parse_u32_trim_trailing(a_s, &a) {
    check write_error()
    return Ok(void)
  }
  if !parse_u32_trim_trailing(b_s, &b) {
    check write_error()
    return Ok(void)
  }
  if b == 0 {
    check write_error()
    return Ok(void)
  }

  let q: u32 = a / b
  check write_u32_line(q)
  return Ok(void)
}
```