```zero
use std

fn is_trailing_ws(b: u8) -> bool {
  if b == 32u8 {
    return true
  }
  if b == 9u8 {
    return true
  }
  if b == 10u8 {
    return true
  }
  if b == 13u8 {
    return true
  }
  return false
}

fn trim_trailing_ws(s: Span<u8>) -> Span<u8> {
  let mut end: usize = s.len()
  while end > 0 {
    let c = s[end - 1]
    if is_trailing_ws(c) {
      end = end - 1
    } else {
      break
    }
  }
  return s[0..end]
}

fn write_error() -> Result<void> {
  check world.out.write("error\n")
  return Ok(())
}

fn print_u32(mut n: u32) -> Result<void> {
  if n >= 10u32 {
    let q: u32 = n / 10u32
    check print_u32(q)
  }
  let d: u32 = n % 10u32
  let mut one: [u8; 1]
  one[0] = 48u8 + (d as u8)
  check world.out.write(one[0..1])
  return Ok(())
}

fn parse_u32_strict(s_in: Span<u8>, out_val: &mut u32) -> bool {
  let s = trim_trailing_ws(s_in)
  let n = s.len()
  if n == 0 {
    return false
  }
  let mut i: usize = 0
  let mut v: u64 = 0u64
  while i < n {
    let c = s[i]
    if c < 48u8 || c > 57u8 {
      return false
    }
    let d: u64 = (c as u64) - 48u64
    v = v * 10u64 + d
    if v > 4294967295u64 {
      return false
    }
    i = i + 1
  }
  *out_val = v as u32
  return true
}

fn main() -> Result<void> {
  let args = std.args()
  let argc = args.len()
  if argc < 2 {
    check write_error()
    return Ok(())
  }

  // Parse N
  let mut N: u32 = 0u32
  if !parse_u32_strict(args[1], &mut N) {
    check write_error()
    return Ok(())
  }
  if N > 1000u32 {
    check write_error()
    return Ok(())
  }

  let need: usize = 2usize + (N as usize)
  if argc < need {
    check write_error()
    return Ok(())
  }

  let mut sum: u64 = 0u64
  let mut i: u32 = 0u32
  while i < N {
    let idx: usize = 2usize + (i as usize)
    let mut val: u32 = 0u32
    if !parse_u32_strict(args[idx], &mut val) {
      check write_error()
      return Ok(())
    }
    let v64: u64 = val as u64
    if sum > 4294967295u64 - v64 {
      check write_error()
      return Ok(())
    }
    sum = sum + v64
    i = i + 1u32
  }

  check print_u32(sum as u32)
  check world.out.write("\n")
  return Ok(())
}
```