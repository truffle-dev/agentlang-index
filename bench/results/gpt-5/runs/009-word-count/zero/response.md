```zero
use std.args

fn is_ws(b: u8) -> bool {
  if b == 0x20 { return true }
  if b == 0x09 { return true }
  if b == 0x0A { return true }
  if b == 0x0D { return true }
  return false
}

fn u64_to_dec(mut x: u64, buf: MutSpan<u8>) -> u64 {
  if x == 0 {
    if buf.len >= 1 {
      buf[0] = 0x30
      return 1
    } else {
      return 0
    }
  }
  var i: u64 = 0
  while x != 0 {
    let d = x % 10
    x = x / 10
    let ch: u8 = 0x30 + (d as u8)
    buf[i] = ch
    i += 1
  }
  var j: u64 = 0
  while j < (i / 2) {
    let lo = j
    let hi = i - 1 - j
    let tmp = buf[lo]
    buf[lo] = buf[hi]
    buf[hi] = tmp
    j += 1
  }
  return i
}

fn main() {
  let argv = args.all()

  var count: u64 = 0
  if argv.len >= 2 {
    let s = argv[1]
    let n = s.len
    var in_word: bool = false
    var i: u64 = 0
    while i < n {
      let b = s[i]
      if is_ws(b) {
        in_word = false
      } else {
        if !in_word {
          count += 1
          in_word = true
        }
      }
      i += 1
    }
  }

  var out: [u8; 32]
  let wrote = u64_to_dec(count, out[0..32])
  out[wrote] = 0x0A
  check world.out.write(out[0..(wrote + 1)])
  return
}
```