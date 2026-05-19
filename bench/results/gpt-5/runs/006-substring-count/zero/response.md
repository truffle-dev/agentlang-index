```zero
use std

fn count_non_overlapping(p: Span<u8>, t: Span<u8>) -> u32 {
  let m: u32 = p.len
  let n: u32 = t.len
  if m == 0 {
    return 0
  }
  let i: u32 = 0
  let c: u32 = 0
  while i + m <= n {
    let j: u32 = 0
    let matched: bool = true
    while j < m {
      if t[i + j] != p[j] {
        matched = false
        break
      }
      j = j + 1
    }
    if matched {
      c = c + 1
      i = i + m
    } else {
      i = i + 1
    }
  }
  return c
}

fn write_u32_line(x: u32) -> void {
  if x == 0 {
    check world.out.write("0\n")
    return
  }
  let buf: [32]u8
  let pos: u32 = 32
  let v: u32 = x
  while v > 0 {
    let d: u32 = v % 10
    let ch: u8 = (48 + d) as u8
    pos = pos - 1
    buf[pos] = ch
    v = v / 10
  }
  check world.out.write(buf[pos..32])
  check world.out.write("\n")
  return
}

fn main() -> void {
  let argc: u32 = std.args.count()
  let p: Span<u8>
  let t: Span<u8>
  if argc >= 3 {
    p = std.args.get(1)
    t = std.args.get(2)
  } else if argc == 2 {
    p = std.args.get(0)
    t = std.args.get(1)
  } else {
    check world.out.write("error\n")
    return
  }

  let cnt: u32 = count_non_overlapping(p, t)
  write_u32_line(cnt)
  return
}
```