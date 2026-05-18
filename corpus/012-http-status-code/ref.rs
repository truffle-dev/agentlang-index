use std::io::{self, Read, Write};
use std::time::Duration;

fn main() {
    let mut url = String::new();
    if io::stdin().read_to_string(&mut url).is_err() {
        let _ = io::stdout().write_all(b"error\n");
        return;
    }
    let url = url.trim();

    let agent = ureq::Agent::config_builder()
        .timeout_global(Some(Duration::from_secs(5)))
        .build()
        .new_agent();

    let result = agent.get(url).call();
    let stdout = io::stdout();
    let mut handle = stdout.lock();
    match result {
        Ok(response) => {
            let _ = writeln!(handle, "{}", response.status().as_u16());
        }
        Err(ureq::Error::StatusCode(code)) => {
            let _ = writeln!(handle, "{}", code);
        }
        Err(_) => {
            let _ = handle.write_all(b"error\n");
        }
    }
}
