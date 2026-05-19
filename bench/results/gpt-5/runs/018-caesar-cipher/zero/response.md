```zero
=== zero.json ===
{
  "package": { "name": "t_018_caesar_cipher", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}
=== src/main.0 ===
use lib

fn is_ascii_whitespace(b: u8) -> bool
  return b == 9 || b == 10 || b == 11 || b == 12 || b == 13 || b == 32

fn write_error(world: World) -> None
  check world.out.write("error\n")
  return

fn main(args: Span<Span<u8>>, world: World) -> None
  if args.len < 3
    check world.out.write("error\n")
    return

  let shift_arg = args[1]
  let mut start = 0
  let mut end = shift_arg.len

  while start < end && is_ascii_whitespace(shift_arg[start])
    start = start + 1

  while end > start && is_ascii_whitespace(shift_arg[end - 1])
    end = end - 1

  if start == end
    check world.out.write("error\n")
    return

  let mut value: u32 = 0
  let mut i = start
  while i < end
    let b = shift_arg[i]
    if b < 48 || b > 57
      check world.out.write("error\n")
      return
    value = value * 10 + ((b - 48) as u32)
    if value > 25
      check world.out.write("error\n")
      return
    i = i + 1

  let plaintext = args[2]
  if plaintext.len == 0
    check world.out.write("error\n")
    return

  let n = plaintext.len
  let mut j = 0
  while j < n
    let pb = plaintext[j]
    if !lib.is_lowercase_letter(pb)
      check world.out.write("error\n")
      return
    j = j + 1

  let mut out: MutSpan<u8> = check world.alloc(n)
  let mut k = 0
  while k < n
    out[k] = lib.shift_letter(plaintext[k], value)
    k = k + 1

  check world.out.write(out[0..n])
  check world.out.write("\n")
  return
=== src/lib.0 ===
export fn is_lowercase_letter(b: u8) -> bool
  return b >= 97 && b <= 122

export fn shift_letter(b: u8, shift: u32) -> u8
  let base: u32 = 97
  let offset: u32 = (b as u32) - base
  let s: u32 = shift % 26
  let new_offset: u32 = (offset + s) % 26
  return (base + new_offset) as u8
```