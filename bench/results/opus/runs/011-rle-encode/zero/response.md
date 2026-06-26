```zero
fn main() {
  let args = std.args()
  if args.len() < 2 {
    return
  }
  let input = args[1]
  let bytes = input.bytes()
  let n = bytes.len()
  if n == 0 {
    return
  }
  let i: u32 = 0
  while i < n {
    let cur = bytes[i]
    let count: u32 = 1
    let j = i + 1
    while j < n {
      if bytes[j] == cur {
        count = count + 1
        j = j + 1
      } else {
        break
      }
    }
    let count_str = u32_to_string(count)
    let byte_str = u32_to_string(@as(u32, cur))
    check world.out.write(count_str)
    check world.out.write(" ")
    check world.out.write(byte_str)
    check world.out.write("\n")
    i = j
  }
  return
}

fn u32_to_string(val: u32) -> String {
  if val == 0 {
    return "0"
  }
  let buf: [10]u8 = undefined
  let pos: u32 = 10
  let v = val
  while v > 0 {
    pos = pos - 1
    buf[pos] = @as(u8, v % 10) + 48
    v = v / 10
  }
  return String.from_bytes(buf[pos..10])
}
```