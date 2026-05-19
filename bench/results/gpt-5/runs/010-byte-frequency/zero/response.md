```zero
use std

write_u64(mut n: u64, world: World) {
  if n == 0 {
    check world.out.write("0")
    return
  }
  let mut buf: [u8; 20]
  let mut i: u64 = 0
  while n > 0 {
    let d: u8 = (n % 10) as u8
    buf[i] = 48 + d
    i = i + 1
    n = n / 10
  }
  while i > 0 {
    i = i - 1
    check world.out.write(buf[i..i+1])
  }
  return
}

main(args: Span<Span<u8>>, world: World) {
  let mut counts: [u64; 256] = [0u64; 256]

  let mut input: Span<u8> = ""
  if args.len() >= 2 {
    input = args[1]
  }

  let n = input.len()
  let mut i: u64 = 0
  while i < n {
    let b: u8 = input[i]
    let idx: u64 = b as u64
    counts[idx] = counts[idx] + 1
    i = i + 1
  }

  let mut v: u64 = 0
  while v < 256 {
    let c: u64 = counts[v]
    if c != 0 {
      check write_u64(v, world)
      check world.out.write(" ")
      check write_u64(c, world)
      check world.out.write("\n")
    }
    v = v + 1
  }

  return
}
```