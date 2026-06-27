```rust
use std::io::{self, Read, Write};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut lines = input.lines();
    let url = lines.next().unwrap_or("").trim().to_string();
    let a: i32 = lines.next().unwrap_or("").trim().parse().unwrap_or(0);
    let b: i32 = lines.next().unwrap_or("").trim().parse().unwrap_or(0);

    let body = format!("{{\"a\":{},\"b\":{}}}", a, b);

    let result = do_request(&url, &body);
    let out = match result {
        Some(sum) => format!("{}\n", sum),
        None => "error\n".to_string(),
    };
    io::stdout().write_all(out.as_bytes()).unwrap();
}

fn do_request(url: &str, body: &str) -> Option<i64> {
    use std::time::Duration;
    let client = ureq::AgentBuilder::new()
        .timeout(Duration::from_millis(5000))
        .build();

    let resp = client
        .post(url)
        .set("Content-Type", "application/json")
        .send_string(body)
        .ok()?;

    if resp.status() != 200 {
        return None;
    }

    let text = resp.into_string().ok()?;
    let val: serde_json::Value = serde_json::from_str(&text).ok()?;
    let sum = val.get("sum")?.as_i64()?;
    Some(sum)
}
```