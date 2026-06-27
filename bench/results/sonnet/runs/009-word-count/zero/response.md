```zero
fn main() {
  let args = std.args()
  if args.len() < 2 {
    check world.out.write("0\n")
    return
  }
  let input = args[1]
  let bytes = input.bytes()
  let n = bytes.len()
  let count: u64 = 0
  let in_word: bool = false
  let i: u64 = 0
  while i < n {
    let b = bytes[i]
    let is_ws: bool = false
    if b == 0x20 {
      is_ws = true
    }
    if b == 0x09 {
      is_ws = true
    }
    if b == 0x0A {
      is_ws = true
    }
    if b == 0x0D {
      is_ws = true
    }
    if is_ws {
      in_word = false
    }
    if !is_ws {
      if !in_word {
        count = count + 1
        in_word = true
      }
    }
    i = i + 1
  }
  let buf: [u8; 32]
  let s = buf[0..32]
  let written = std.fmt_u64(s, count)
  check world.out.write(buf[0..written])
  check world.out.write("\n")
  return
}
```