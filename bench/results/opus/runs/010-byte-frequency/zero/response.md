```zero
fn main() -> u8
  let args = std.args()
  if args.len() < 2
    return 0

  let input = args[1]
  let bytes = input.bytes()

  mut counts: [256]u32 = undefined
  mut i: u32 = 0
  loop
    if i >= 256
      break
    counts[i] = 0
    i = i + 1

  mut j: u32 = 0
  loop
    if j >= bytes.len()
      break
    let b: u32 = bytes[j]
    counts[b] = counts[b] + 1
    j = j + 1

  mut k: u32 = 0
  loop
    if k >= 256
      break
    if counts[k] > 0
      check world.out.write(str(k))
      check world.out.write(" ")
      check world.out.write(str(counts[k]))
      check world.out.write("\n")
    k = k + 1

  return 0
```