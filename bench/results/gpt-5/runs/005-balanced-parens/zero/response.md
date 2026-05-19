```zero
use std

fn main() -> Error!void
  let args = std.args()
  if args.len == 0
    check world.out.write("yes\n")
    return

  let s = args[0]
  let mut stack: [u8; 1024]
  let mut sp: usize = 0

  let mut i: usize = 0
  let n = s.len
  while i < n
    let b = s[i]
    if b == 40 || b == 91 || b == 123
      if sp >= 1024
        check world.out.write("no\n")
        return
      stack[sp] = b
      sp = sp + 1
    else if b == 41 || b == 93 || b == 125
      if sp == 0
        check world.out.write("no\n")
        return
      sp = sp - 1
      let top = stack[sp]
      if (b == 41 && top != 40) || (b == 93 && top != 91) || (b == 125 && top != 123)
        check world.out.write("no\n")
        return
    i = i + 1

  if sp == 0
    check world.out.write("yes\n")
  else
    check world.out.write("no\n")
  return
```