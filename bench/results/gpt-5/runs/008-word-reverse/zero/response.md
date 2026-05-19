```zero
use std

export fn main() -> void {
  let args = std.args
  let mut wrote = false

  let mut ai: i64 = (args.len as i64) - 1
  while ai >= 0 {
    let s = args[ai as u64]
    let mut i: i64 = (s.len as i64) - 1

    while i >= 0 {
      if s[i as u64] == 32 {
        i = i - 1
      } else {
        break
      }
    }

    while i >= 0 {
      let end = i
      while i >= 0 {
        if s[i as u64] == 32 {
          break
        }
        i = i - 1
      }
      let start: i64 = i + 1

      if wrote {
        check world.out.write(" ")
      } else {
        wrote = true
      }
      check world.out.write(s[start as u64 .. (end + 1) as u64])

      while i >= 0 {
        if s[i as u64] == 32 {
          i = i - 1
        } else {
          break
        }
      }
    }

    ai = ai - 1
  }

  if wrote {
    check world.out.write("\n")
  }

  return
}
```