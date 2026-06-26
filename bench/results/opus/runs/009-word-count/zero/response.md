```zero
fn main() i32
  let args = std.args()
  if args.len() < 2
    check world.out.write("0\n")
    return 0
  let input = args[1]
  let count: i32 = 0
  let in_word = false
  let i: u32 = 0
  while i < input.len()
    let c = input[i]
    if c == 32 or c == 9 or c == 10 or c == 13
      if in_word
        in_word = false
    else
      if not in_word
        in_word = true
        count = count + 1
    i = i + 1
  check world.out.write(int_to_string(count))
  check world.out.write("\n")
  return 0

fn int_to_string(n: i32) String
  if n == 0
    return "0"
  let result = ""
  let val = n
  while val > 0
    let digit = val % 10
    val = val / 10
    if digit == 0
      result = string.concat("0", result)
    else if digit == 1
      result = string.concat("1", result)
    else if digit == 2
      result = string.concat("2", result)
    else if digit == 3
      result = string.concat("3", result)
    else if digit == 4
      result = string.concat("4", result)
    else if digit == 5
      result = string.concat("5", result)
    else if digit == 6
      result = string.concat("6", result)
    else if digit == 7
      result = string.concat("7", result)
    else if digit == 8
      result = string.concat("8", result)
    else
      result = string.concat("9", result)
  return result
```