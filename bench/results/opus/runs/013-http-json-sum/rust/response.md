```rust
use std::io::{self, Read, Write};
use std::net::TcpStream;
use std::time::Duration;

fn run() -> Option<String> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).ok()?;
    let mut lines = input.lines();
    let url = lines.next()?.trim();
    let a: i32 = lines.next()?.trim().parse().ok()?;
    let b: i32 = lines.next()?.trim().parse().ok()?;

    // Parse URL: http://host:port/path
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

    let body = format!("{{\"a\":{},\"b\":{}}}", a, b);
    let request = format!(
        "POST {} HTTP/1.1\r\nHost: {}\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}",
        path, host_port, body.len(), body
    );

    let timeout = Duration::from_millis(5000);
    let addrs: Vec<_> = std::net::ToSocketAddrs::to_socket_addrs(&(host, port)).ok()?.collect();
    if addrs.is_empty() {
        return None;
    }

    let mut stream = None;
    for addr in &addrs {
        if let Ok(s) = TcpStream::connect_timeout(addr, timeout) {
            stream = Some(s);
            break;
        }
    }
    let mut stream = stream?;
    stream.set_read_timeout(Some(timeout)).ok()?;
    stream.set_write_timeout(Some(timeout)).ok()?;
    stream.write_all(request.as_bytes()).ok()?;

    let mut response = Vec::new();
    loop {
        let mut buf = [0u8; 4096];
        match stream.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => response.extend_from_slice(&buf[..n]),
            Err(e) if e.kind() == io::ErrorKind::Interrupted => continue,
            Err(_) => break,
        }
    }

    let resp_str = String::from_utf8_lossy(&response);
    let header_end = resp_str.find("\r\n\r\n")?;
    let header_part = &resp_str[..header_end];
    let body_part = &response[header_end + 4..];

    // Check status line
    let status_line = header_part.lines().next()?;
    let mut parts = status_line.splitn(3, ' ');
    parts.next()?; // HTTP/1.x
    let status: u16 = parts.next()?.parse().ok()?;
    if status != 200 {
        return None;
    }

    // Parse body as JSON - minimal parser for {"sum": <integer>}
    let body_str = std::str::from_utf8(body_part).ok()?.trim();
    // Find "sum" field
    let sum = parse_sum(body_str)?;

    Some(format!("{}", sum))
}

fn parse_sum(json: &str) -> Option<i32> {
    // Minimal JSON object parser: find "sum" key and extract integer value
    let s = json.trim();
    if !s.starts_with('{') || !s.ends_with('}') {
        return None;
    }
    // Find "sum" key
    let mut i = 0;
    let bytes = s.as_bytes();
    while i < bytes.len() {
        // Find next quoted string
        if bytes[i] == b'"' {
            let start = i + 1;
            i += 1;
            while i < bytes.len() && bytes[i] != b'"' {
                if bytes[i] == b'\\' { i += 1; }
                i += 1;
            }
            let key = &s[start..i];
            i += 1; // skip closing quote
            // skip whitespace and colon
            while i < bytes.len() && (bytes[i] == b' ' || bytes[i] == b'\t' || bytes[i] == b'\n' || bytes[i] == b'\r') { i += 1; }
            if i < bytes.len() && bytes[i] == b':' {
                i += 1;
                while i < bytes.len() && (bytes[i] == b' ' || bytes[i] == b'\t' || bytes[i] == b'\n' || bytes[i] == b'\r') { i += 1; }
                if key == "sum" {
                    // Extract the value - should be an integer
                    let val_start = i;
                    if i < bytes.len() && (bytes[i] == b'-' || bytes[i].is_ascii_digit()) {
                        if bytes[i] == b'-' { i += 1; }
                        while i < bytes.len() && bytes[i].is_ascii_digit() { i += 1; }
                        // Must not be followed by '.' (float)
                        if i < bytes.len() && bytes[i] == b'.' { return None; }
                        let val_str = &s[val_start..i];
                        return val_str.parse::<i32>().ok();
                    }
                    return None;
                } else {
                    // Skip this value
                    i = skip_json_value(bytes, i)?;
                }
            }
        } else {
            i += 1;
        }
    }
    None
}

fn skip_json_value(bytes: &[u8], mut i: usize) -> Option<usize> {
    if i >= bytes.len() { return None; }
    match bytes[i] {
        b'"' => {
            i += 1;
            while i < bytes.len() && bytes[i] != b'"' {
                if bytes[i] == b'\\' { i += 1; }
                i += 1;
            }
            Some(i + 1)
        }
        b'{' => {
            let mut depth = 1;
            i += 1;
            while i < bytes.len() && depth > 0 {
                if bytes[i] == b'{' { depth += 1; }
                else if bytes[i] == b'}' { depth -= 1; }
                else if bytes[i] == b'"' {
                    i += 1;
                    while i < bytes.len() && bytes[i] != b'"' {
                        if bytes[i] == b'\\' { i += 1; }
                        i += 1;
                    }
                }
                i += 1;
            }
            Some(i)
        }
        b'[' => {
            let mut depth = 1;
            i += 1;
            while i < bytes.len() && depth > 0 {
                if bytes[i] == b'[' { depth += 1; }
                else if bytes[i] == b']' { depth -= 1; }
                else if bytes[i] == b'"' {
                    i += 1;
                    while i < bytes.len() && bytes[i] != b'"' {
                        if bytes[i] == b'\\' { i += 1; }
                        i += 1;
                    }
                }
                i += 1;
            }
            Some(i)
        }
        b't' => Some(i + 4), // true
        b'f' => Some(i + 5), // false
        b'n' => Some(i + 4), // null
        _ if bytes[i] == b'-' || bytes[i].is_ascii_digit() => {
            while i < bytes.len() && (bytes[i].is_ascii_digit() || bytes[i] == b'-' || bytes[i] == b'.' || bytes[i] == b'e' || bytes[i] == b'E' || bytes[i] == b'+') {
                i += 1;
            }
            Some(i)
        }
        _ => Some(i + 1),
    }
}

fn main() {
    let result = run().unwrap_or_else(|| "error".to_string());
    let out = format!("{}\n", result);
    io::stdout().write_all(out.as_bytes()).unwrap();
}
```