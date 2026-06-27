```zero
fn main() {
  let args = std.args

  let stack: [u8; 1001] = [0; 1001]
  let sp: u64 = 0
  let balanced: bool = true

  let input: Span<u8> = ""
  if args.len > 0 {
    input = args[0]
  }

  let i: u64 = 0
  while i < input.len {
    if balanced {
      let c: u8 = input[i]
      if c == 40u8 || c == 91u8 || c == 123u8 {
        stack[sp] = c
        sp = sp + 1
      } else if c == 41u8 {
        if sp == 0 || stack[sp - 1] != 40u8 {
          balanced = false
        } else {
          sp = sp - 1
        }
      } else if c == 93u8 {
        if sp == 0 || stack[sp - 1] != 91u8 {
          balanced = false
        } else {
          sp = sp - 1
        }
      } else if c == 125u8 {
        if sp == 0 || stack[sp - 1] != 123u8 {
          balanced = false
        } else {
          sp = sp - 1
        }
      }
    }
    i = i + 1
  }

  if balanced && sp == 0 {
    check world.out.write("yes\n")
  } else {
    check world.out.write("no\n")
  }

  return
}
```