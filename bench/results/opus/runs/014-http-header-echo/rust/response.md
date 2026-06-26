```rust
use std::io::{self, Read, Write};
use std::net::TcpStream;
use std::time::Duration;

fn run() -> Option<String> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok()?;
    let mut lines = input.lines();
    let url = lines.next()?.trim();
    let header_name = lines.next()?.trim();

    // Parse URL: only support http://
    let rest = url.strip_prefix("http://")?;
    let (host_port, path) = match rest.find('/') {
        Some(i) => (&rest[..i], &rest[i..]),
        None => (rest, "/"),
    };

    let (host, port) = if let Some(i) = host_port.rfind(':') {
        (&host_port[..i], host_port[i+1..].parse::<u16>().ok()?)
    } else {
        (host_port, 80u16)
    };

    let timeout = Duration::from_millis(5000);
    let stream = TcpStream::connect_timeout(
        &format!("{}:{}", host, port).parse().ok()?,
        timeout,
    ).ok()?;
    stream.set_read_timeout(Some(timeout)).ok()?;
    stream.set_write_timeout(Some(timeout)).ok()?;

    let mut stream = stream;
    let request = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n",
        path, host_port
    );
    stream.write_all(request.as_bytes()).ok()?;

    let mut response = Vec::new();
    stream.read_to_end(&mut response).ok()?;

    let resp_str = String::from_utf8_lossy(&response);
    let header_end = resp_str.find("\r\n\r\n")?;
    let header_section = &resp_str[..header_end];

    let mut lines_iter = header_section.lines();
    let status_line = lines_iter.next()?;
    // e.g. "HTTP/1.1 200 OK"
    let mut parts = status_line.split_whitespace();
    parts.next()?; // HTTP/1.x
    let code: u16 = parts.next()?.parse().ok()?;
    if code != 200 {
        return None;
    }

    let search = header_name.to_ascii_lowercase();
    for line in lines_iter {
        if let Some(colon) = line.find(':') {
            let name = &line[..colon];
            if name.eq_ignore_ascii_case(&search) {
                let value = line[colon+1..].trim();
                return Some(value.to_string());
            }
        }
    }

    None
}

fn main() {
    let out = io::stdout();
    let mut out = out.lock();
    match run() {
        Some(val) => { let _ = writeln!(out, "{}", val); }
        None => { let _ = writeln!(out, "error"); }
    }
}
```