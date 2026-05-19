```zero
use std

fn parse_u32(s: Span<u8>) -> u32 {
  let mut i: usize = 0
  let n = s.len
  let mut val: u32 = 0
  while i < n {
    let c = s[i]
    if c < 48 || c > 57 {
      break
    }
    val = val * 10 + (c - 48) as u32
    i = i + 1
  }
  return val
}

export fn main() -> i32 {
  let mut world = std.io.default_world()

  let argv = std.args.all()
  if argv.len == 0 {
    check world.out.write("error\n")
    return 0
  }
  let s = argv[0]
  let n_u32 = parse_u32(s)
  let mut n_usize: usize = n_u32 as usize
  if n_usize > 10000 {
    n_usize = 10000
  }

  let mut is_prime: [u8; 10001]
  let mut i: usize = 0
  while i <= n_usize {
    is_prime[i] = 1
    i = i + 1
  }
  if n_usize >= 0 {
    is_prime[0] = 0
  }
  if n_usize >= 1 {
    is_prime[1] = 0
  }

  let mut p: usize = 2
  while p * p <= n_usize {
    if is_prime[p] != 0 {
      let mut m: usize = p * p
      while m <= n_usize {
        is_prime[m] = 0
        m = m + p
      }
    }
    p = p + 1
  }

  let mut cnt: u32 = 0
  let mut k: usize = 2
  while k <= n_usize {
    if is_prime[k] != 0 {
      cnt = cnt + 1
    }
    k = k + 1
  }

  let mut buf: [u8; 32]
  let mut blen: usize = 0
  if cnt == 0 {
    buf[0] = 48
    blen = 1
  } else {
    let mut x: u32 = cnt
    while x > 0 {
      let d = (x % 10) as u8
      buf[blen] = 48 + d
      blen = blen + 1
      x = x / 10
    }
    let mut a: usize = 0
    let mut b: usize = blen - 1
    while a < b {
      let t = buf[a]
      buf[a] = buf[b]
      buf[b] = t
      a = a + 1
      b = b - 1
    }
  }
  buf[blen] = 10
  blen = blen + 1
  check world.out.write(buf[0..blen])

  return 0
}
```