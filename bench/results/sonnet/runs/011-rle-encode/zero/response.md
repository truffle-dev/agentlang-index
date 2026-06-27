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
  let i = 0u64
  let run_byte = bytes[0]
  let run_count = 1u64
  i = 1
  while i < n {
    let b = bytes[i]
    if b == run_byte {
      run_count = run_count + 1
    } else {
      let line = run_count.str() ++ " " ++ run_byte.str() ++ "\n"
      check world.out.write(line)
      run_byte = b
      run_count = 1
    }
    i = i + 1
  }
  let line = run_count.str() ++ " " ++ run_byte.str() ++ "\n"
  check world.out.write(line)
  return
}
```