```
=== zero.json ===
{
  "package": { "name": "t_019_run_length_encode", "version": "0.1.0", "license": "MIT" },
  "targets": { "cli": { "kind": "exe", "main": "src/main.0", "defaultTarget": "linux-musl-x64", "devTarget": "host", "releaseProfile": "release-small" } },
  "deps": {}, "profiles": { "dev": { "inherits": "dev" }, "release-small": { "inherits": "release-small" } }
}

=== src/main.0 ===
use lib

export fn main(argv: [str]) -> void {
    if argv.len() != 2 {
        check world.out.write("error\n")
        return
    }
    
    let input = argv[1]
    if input.len() == 0 || input[input.len() - 1] != '\n' {
        check world.out.write("error\n")
        return
    }
    
    let mut i = 0
    let mut result = ""
    while i < input.len() - 1 {
        let current = input[i]
        if !lib.is_lowercase_letter(current) {
            check world.out.write("error\n")
            return
        }
        
        let mut count = 1
        while i + 1 < input.len() - 1 && input[i + 1] == current {
            count += 1
            i += 1
        }
        
        result += current
        result += lib.decimal_length(count)
        
        i += 1
    }
    
    result += "\n"
    check world.out.write(result)
    return
}

=== src/lib.0 ===
export fn is_lowercase_letter(c: u8) -> bool {
    return c >= 'a' && c <= 'z'
}

export fn digit_byte(d: u8) -> u8 {
    return '0' + d
}

export fn decimal_length(n: u32) -> str {
    let mut result = ""
    let mut num = n
    let mut digits = []
    
    while num > 0 {
        let digit = num % 10
        digits.push(lib.digit_byte(digit as u8))
        num /= 10
    }
    
    let mut i = digits.len()
    while i > 0 {
        i -= 1
        result += digits[i]
    }
    
    return result
}
```