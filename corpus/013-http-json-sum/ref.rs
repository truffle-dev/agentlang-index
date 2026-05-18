// HTTP POST + JSON sum reference for AgentLang Index.

use std::io::{self, Read};
use std::time::Duration;

fn fail() {
    print!("error\n");
}

fn run() -> Option<i64> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok()?;
    let mut lines = input.lines();
    let url = lines.next()?.trim().to_string();
    let a: i64 = lines.next()?.trim().parse().ok()?;
    let b: i64 = lines.next()?.trim().parse().ok()?;
    let body = format!("{{\"a\":{},\"b\":{}}}", a, b);

    let agent = ureq::Agent::config_builder()
        .timeout_global(Some(Duration::from_secs(5)))
        .build()
        .new_agent();

    let response = agent
        .post(&url)
        .header("Content-Type", "application/json")
        .send(body.as_bytes());

    let mut response = match response {
        Ok(r) => r,
        Err(_) => return None,
    };
    if response.status().as_u16() != 200 {
        return None;
    }
    let body_text = response.body_mut().read_to_string().ok()?;
    let parsed: serde_json::Value = serde_json::from_str(&body_text).ok()?;
    let obj = parsed.as_object()?;
    let sum_val = obj.get("sum")?;
    let s = sum_val.as_i64()?;
    Some(s)
}

fn main() {
    match run() {
        Some(s) => print!("{}\n", s),
        None => fail(),
    }
}
