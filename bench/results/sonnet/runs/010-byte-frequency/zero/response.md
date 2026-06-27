```zero
fn write_num(n: u64) {
  if n == 0 {
    check world.out.write("0")
    return
  }
  let buf = [20]u8
  let pos: u64 = 20
  let m: u64 = n
  while m > 0 {
    pos = pos - 1
    buf[pos] = (m % 10) as u8 + 48u8
    m = m / 10
  }
  check world.out.write(buf[pos..20])
  return
}

fn main() {
  let args = std.args()
  let input = args[1]
  let counts = [256]u64
  let i: u64 = 0
  while i < input.len {
    let b = input[i] as u64
    counts[b] = counts[b] + 1
    i = i + 1
  }
  let v: u64 = 0
  while v < 256 {
    if counts[v] > 0 {
      write_num(v)
      check world.out.write(" ")
      write_num(counts[v])
      check world.out.write("\n")
    }
    v = v + 1
  }
  return
}
```