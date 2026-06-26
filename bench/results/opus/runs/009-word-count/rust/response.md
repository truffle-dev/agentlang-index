```rust
use std::io::Read;
fn main(){
    let mut buf=String::new();
    std::io::stdin().read_to_string(&mut buf).unwrap();
    let c=buf.split_ascii_whitespace().count();
    std::io::stdout().write_all(format!("{c}\n").as_bytes()).unwrap();
}
```