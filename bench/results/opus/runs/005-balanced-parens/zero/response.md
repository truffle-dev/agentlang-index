```zero
fn main(world: World) -> u8
  let args = std.args()
  let input: String = ""
  if args.len() > 1
    input = args[1]
  let stack: Array(u8, 1001) = undefined
  let top: i32 = 0
  let balanced: bool = true
  let i: i32 = 0
  while i < input.len()
    let c = input[i]
    if c == '(' or c == '[' or c == '{'
      stack[top] = c
      top = top + 1
    if c == ')'
      if top == 0
        balanced = false
      else
        top = top - 1
        if stack[top] != '('
          balanced = false
    if c == ']'
      if top == 0
        balanced = false
      else
        top = top - 1
        if stack[top] != '['
          balanced = false
    if c == '}'
      if top == 0
        balanced = false
      else
        top = top - 1
        if stack[top] != '{'
          balanced = false
    i = i + 1
  if top != 0
    balanced = false
  if balanced
    check world.out.write("yes\n")
  else
    check world.out.write("no\n")
  return 0
```