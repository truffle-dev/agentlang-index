```zero
use std.{world, args}

fn min3(a: u16, b: u16, c: u16) -> u16 {
  let mut m = a
  if b < m {
    m = b
  }
  if c < m {
    m = c
  }
  return m
}

export fn main() void {
  let argv = args.list()
  let argc = argv.len
  if argc != 2 {
    check world.out.write("error\n")
    return
  }

  let A = argv[0]
  let B = argv[1]

  let n = A.len
  let m = B.len

  // Limit to ensure our fixed-size rows are sufficient
  if m > 2048 || n > 2048 {
    check world.out.write("error\n")
    return
  }

  // Two DP rows: size m+1, we provision a safe upper bound
  const MAXCOL = 2049
  let mut prev: [MAXCOL]u16
  let mut curr: [MAXCOL]u16

  // Initialize first row: distance from empty A prefix to B[0..j]
  let mut j: usize = 0
  while j <= m {
    prev[j] = j as u16
    j = j + 1
  }

  let mut i: usize = 1
  while i <= n {
    curr[0] = i as u16

    let ai = A[i - 1]

    let mut jj: usize = 1
    while jj <= m {
      let bj = B[jj - 1]
      let mut cost: u16 = 1
      if ai == bj {
        cost = 0
      }

      let del = (prev[jj] as u32 + 1) as u16
      let ins = (curr[jj - 1] as u32 + 1) as u16
      let sub = (prev[jj - 1] as u32 + (cost as u32)) as u16

      curr[jj] = min3(del, ins, sub)

      jj = jj + 1
    }

    // copy curr to prev
    let mut k: usize = 0
    while k <= m {
      prev[k] = curr[k]
      k = k + 1
    }

    i = i + 1
  }

  let dist = prev[m] as u32

  // Convert dist to decimal string and write with trailing newline
  let mut buf: [32]u8
  let mut idx: usize = 0
  if dist == 0 {
    buf[0] = 48  // '0'
    idx = 1
  } else {
    let mut x: u32 = dist
    while x > 0 {
      let d = (x % 10) as u8
      buf[idx] = 48 + d
      idx = idx + 1
      x = x / 10
    }
    // reverse digits in-place
    let mut l: usize = 0
    let mut r: usize = idx
    if r > 0 {
      r = r - 1
    }
    while l < r {
      let tmp = buf[l]
      buf[l] = buf[r]
      buf[r] = tmp
      l = l + 1
      if r == 0 {
        // shouldn't happen because l<r, but guard against underflow
        break
      }
      r = r - 1
    }
  }
  buf[idx] = 10  // '\n'
  idx = idx + 1
  check world.out.write(buf[0..idx])

  return
}
```