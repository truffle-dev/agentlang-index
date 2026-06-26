```zero
=== zero.json ===
{
  "package": { "name": "t_018_caesar_cipher", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/lib.0 ===
pub fn is_lowercase_letter(c: u8) bool =
  if c >= 'a'
    if c <= 'z'
      return true
    end
  end
  return false

pub fn shift_letter(c: u8, shift: u8) u8 =
  let offset: u8 = c - 'a'
  let shifted: u8 = (offset + shift) % 26
  return shifted + 'a'

=== src/main.0 ===
use lib

fn main() void =
  let args = world.args()
  if args.len() != 3
    check world.out.write("error\n")
    return
  end

  let shift_str = args[1]
  let plaintext = args[2]

  // validate shift string: must be non-empty, all digits
  if shift_str.len() == 0
    check world.out.write("error\n")
    return
  end

  // trim trailing whitespace from shift_str
  let trim_len: u32 = shift_str.len()
  loop
    if trim_len == 0
      break
    end
    let ch = shift_str[trim_len - 1]
    if ch == ' '
      trim_len = trim_len - 1
    else
      if ch == '\t'
        trim_len = trim_len - 1
      else
        if ch == '\r'
          trim_len = trim_len - 1
        else
          if ch == '\n'
            trim_len = trim_len - 1
          else
            break
          end
        end
      end
    end
  end

  if trim_len == 0
    check world.out.write("error\n")
    return
  end

  // parse shift value
  let shift_val: u32 = 0
  let i: u32 = 0
  loop
    if i >= trim_len
      break
    end
    let d = shift_str[i]
    if d < '0'
      check world.out.write("error\n")
      return
    end
    if d > '9'
      check world.out.write("error\n")
      return
    end
    shift_val = shift_val * 10 + (d - '0')
    i = i + 1
  end

  if shift_val > 25
    check world.out.write("error\n")
    return
  end

  // validate plaintext: must be non-empty, all lowercase
  if plaintext.len() == 0
    check world.out.write("error\n")
    return
  end

  let j: u32 = 0
  loop
    if j >= plaintext.len()
      break
    end
    if !lib.is_lowercase_letter(plaintext[j])
      check world.out.write("error\n")
      return
    end
    j = j + 1
  end

  // produce ciphertext
  let shift8: u8 = shift_val
  var buf: [1024]u8 = undefined
  let k: u32 = 0
  loop
    if k >= plaintext.len()
      break
    end
    buf[k] = lib.shift_letter(plaintext[k], shift8)
    k = k + 1
  end
  buf[k] = '\n'
  check world.out.write(buf[0..k + 1])
  return
```