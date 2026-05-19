```zero
=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}
=== src/main.0 ===
use world
use lib

export fn main() -> void {
  let args = world.args()
  if args.len() < 2u32 {
    check world.out.write("error\n")
    return
  }

  let input = args[1u32]
  let n = input.len()

  if n == 0u32 {
    check world.out.write("error\n")
    return
  }

  let last = input[n - 1u32]
  if last != 10u8 {
    check world.out.write("error\n")
    return
  }

  let m = n - 1u32
  if m == 0u32 {
    check world.out.write("error\n")
    return
  }

  let mut i = 0u32
  while i < m {
    let b = input[i]
    if lib.is_lowercase_letter(b) {
      // ok
    } else {
      check world.out.write("error\n")
      return
    }
    i = i + 1u32
  }

  let mut one: [1]u8
  i = 0u32
  while i < m {
    let ch = input[i]
    let mut run: u64 = 1u64
    let mut j = i + 1u32
    while j < m {
      if input[j] == ch {
        run = run + 1u64
        j = j + 1u32
      } else {
        break
      }
    }

    one[0u32] = ch
    check world.out.write(one[0u32..1u32])

    let d = lib.decimal_length(run)
    let mut p: u64 = 1u64
    let mut k: u32 = 1u32
    while k < d {
      p = p * 10u64
      k = k + 1u32
    }
    while p > 0u64 {
      let q = run / p
      let dig64 = q % 10u64
      let dig = dig64 as u32
      let db = lib.digit_byte(dig)
      one[0u32] = db
      check world.out.write(one[0u32..1u32])
      p = p / 10u64
    }

    i = j
  }

  one[0u32] = 10u8
  check world.out.write(one[0u32..1u32])
  return
}
=== src/lib.0 ===
export fn is_lowercase_letter(b: u8) -> bool {
  let mut ok = false
  if b >= 97u8 {
    if b <= 122u8 {
      ok = true
    }
  }
  return ok
}

export fn digit_byte(d: u32) -> u8 {
  return 48u8 + (d as u8)
}

export fn decimal_length(x: u64) -> u32 {
  if x == 0u64 {
    return 1u32
  }
  let mut n = x
  let mut c: u32 = 0u32
  while n > 0u64 {
    c = c + 1u32
    n = n / 10u64
  }
  return c
}
```