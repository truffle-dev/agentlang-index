```zero
use std

fn parse_i64(s: Span<u8>) -> i64 {
  let mut i = 0
  let n = s.len
  let mut sign: i64 = 1
  if n > 0 && s[0] == 45 {
    sign = -1
    i = 1
  }
  let mut v: i64 = 0
  while i < n {
    let c = s[i]
    v = v * 10 + ((c - 48) as i64)
    i = i + 1
  }
  return v * sign
}

fn write_i64(mut x: i64) {
  let mut buf: [u8; 32]
  let mut len = 0
  if x == 0 {
    buf[0] = 48
    len = 1
  } else {
    let mut neg = false
    if x < 0 {
      neg = true
      x = -x
    }
    let mut p = 0
    while x > 0 {
      let d = (x % 10) as i64
      buf[p] = (48 + (d as u8))
      x = x / 10
      p = p + 1
    }
    if neg {
      buf[p] = 45
      p = p + 1
    }
    let mut l = 0
    let mut r = p - 1
    while l < r {
      let t = buf[l]
      buf[l] = buf[r]
      buf[r] = t
      l = l + 1
      r = r - 1
    }
    len = p
  }
  check world.out.write(buf[0..len])
}

pub fn main() -> i32 {
  let args = std.args
  let n = parse_i64(args[0]) as i32
  let nn = (n as i32) * (n as i32)

  let mut A: [i64; 25]
  let mut B: [i64; 25]

  let mut idx = 0
  while idx < nn {
    A[idx] = parse_i64(args[1 + idx])
    idx = idx + 1
  }

  let mut jdx = 0
  while jdx < nn {
    B[jdx] = parse_i64(args[1 + nn + jdx])
    jdx = jdx + 1
  }

  let mut i = 0
  while i < n {
    let mut j = 0
    while j < n {
      let mut sum: i64 = 0
      let mut k = 0
      while k < n {
        let a = A[(i * n + k) as i32]
        let b = B[(k * n + j) as i32]
        sum = sum + a * b
        k = k + 1
      }
      if j > 0 {
        check world.out.write(" ")
      }
      write_i64(sum)
      j = j + 1
    }
    check world.out.write("\n")
    i = i + 1
  }

  return 0
}
```