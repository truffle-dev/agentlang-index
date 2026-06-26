```zero
=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {},
  "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/lib.0 ===
pub fn is_lowercase_letter(b: u8) bool =
  if b >= 97
    if b <= 122
      return true
    end
    return false
  end
  return false

pub fn digit_byte(d: u8) u8 =
  return d + 48

pub fn decimal_length(n: u32) u32 =
  if n < 10
    return 1
  end
  if n < 100
    return 2
  end
  if n < 1000
    return 3
  end
  if n < 10000
    return 4
  end
  return 5

=== src/main.0 ===
use lib

fn main(world: World) i32 =
  let args = world.args()
  if args.len < 2
    check world.out.write("error\n")
    return 0
  end
  let input = args[1]
  let len = input.len
  if len == 0
    check world.out.write("error\n")
    return 0
  end
  let i: u32 = 0
  while i < len
    let b = input[i]
    if lib.is_lowercase_letter(b) == false
      check world.out.write("error\n")
      return 0
    end
    i = i + 1
  end
  i = 0
  while i < len
    let cur = input[i]
    let run_start = i
    i = i + 1
    while i < len
      if input[i] == cur
        i = i + 1
      else
        break
      end
    end
    let run_len = i - run_start
    var buf: [6]u8 = undefined
    buf[0] = cur
    let dlen = lib.decimal_length(run_len)
    var rem = run_len
    var pos = dlen
    while pos > 0
      pos = pos - 1
      let d: u8 = @truncate(rem % 10)
      buf[1 + pos] = lib.digit_byte(d)
      rem = rem / 10
    end
    check world.out.write(buf[0 .. 1 + dlen])
  end
  check world.out.write("\n")
  return 0
```