```zero
use std

u64_to_dec = fn(n: u64, out: MutSpan<u8>) -> usize {
  if n == 0u64 {
    out[0] = 48u8
    return 1usize
  }

  let mut x = n
  let mut tmp: [u8; 20]
  let mut i: usize = 0usize
  while x > 0u64 {
    let digit = (x % 10u64) as u8
    tmp[i] = digit + 48u8
    i = i + 1usize
    x = x / 10u64
  }

  let len = i
  let mut j: usize = 0usize
  while j < len {
    out[j] = tmp[len - 1usize - j]
    j = j + 1usize
  }
  return len
}

main = fn() -> Result<(), ()> {
  let args = std.args()
  let argc = args.len
  if argc < 2usize {
    return
  }

  let input = args[1]
  let n = input.len
  if n == 0usize {
    return
  }

  let mut numbuf: [u8; 32]

  let mut prev = input[0]
  let mut count: u64 = 1u64

  let mut i: usize = 1usize
  while i < n {
    let b = input[i]
    if b == prev {
      count = count + 1u64
    } else {
      let len1 = u64_to_dec(count, numbuf[0..])
      check world.out.write(numbuf[0..len1])
      check world.out.write(" ")
      let b_u64: u64 = b as u64
      let len2 = u64_to_dec(b_u64, numbuf[0..])
      check world.out.write(numbuf[0..len2])
      check world.out.write("\n")
      prev = b
      count = 1u64
    }
    i = i + 1usize
  }

  let len1 = u64_to_dec(count, numbuf[0..])
  check world.out.write(numbuf[0..len1])
  check world.out.write(" ")
  let b_u64: u64 = prev as u64
  let len2 = u64_to_dec(b_u64, numbuf[0..])
  check world.out.write(numbuf[0..len2])
  check world.out.write("\n")

  return
}
```