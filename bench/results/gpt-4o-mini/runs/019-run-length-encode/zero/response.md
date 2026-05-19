```zero
=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/main.0 ===
use lib
func main() {
  check world.out.write(run_length_encode(argv[1]))
  return
}

func run_length_encode(input: u8) -> Span<u8> {
  if input.len() == 0 {
    return "error\n"
  }
  var result: [u8; 256] = [0]
  var count: u8 = 1
  var j: usize = 0
  for i in 1..input.len() {
    if !is_lowercase_letter(input[i]) {
      return "error\n"
    }
    if input[i] == input[i - 1] {
      count += 1
    } else {
      j += decimal_length(count, result[j..])
      result[j] = input[i - 1]
      j += 1
      result[j] = count + '0'
      j += 1
      count = 1
    }
  }
  j += decimal_length(count, result[j..])
  result[j] = input[input.len() - 1]
  j += 1
  result[j] = count + '0'
  j += 1
  result[j] = '\n'
  return result[0..j + 1]
}

=== src/lib.0 ===
func is_lowercase_letter(b: u8) -> bool {
  return b >= 'a' && b <= 'z'
}

func decimal_length(n: u8, buf: Span<u8>) -> usize {
  var len: usize = 0
  if n == 0 {
    return len
  }
  var temp: u8 = n
  while temp > 0 {
    len += 1
    temp /= 10
  }
  var i: usize = len
  while n > 0 {
    buf[i - 1] = (n % 10) + '0'
    n /= 10
    i -= 1
  }
  return len
}
```