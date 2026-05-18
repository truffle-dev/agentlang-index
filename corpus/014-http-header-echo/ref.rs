// HTTP header echo reference for AgentLang Index.

use std::io::{self, Read};
use std::time::Duration;

fn fail() {
    print!("error\n");
}

fn run() -> Option<String> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok()?;
    let mut lines = input.lines();
    let url = lines.next()?.trim().to_string();
    let name = lines.next()?.trim().to_string();
    if url.is_empty() || name.is_empty() {
        return None;
    }

    let agent = ureq::Agent::config_builder()
        .timeout_global(Some(Duration::from_secs(5)))
        .build()
        .new_agent();

    let response = agent.get(&url).call();

    let response = match response {
        Ok(r) => r,
        Err(_) => return None,
    };
    if response.status().as_u16() != 200 {
        return None;
    }
    let headers = response.headers();
    let value_opt = headers.get(&name);
    let v = value_opt?;
    v.to_str().ok().map(|s| s.to_string())
}

fn main() {
    match run() {
        Some(s) => print!("{}\n", s),
        None => fail(),
    }
}
