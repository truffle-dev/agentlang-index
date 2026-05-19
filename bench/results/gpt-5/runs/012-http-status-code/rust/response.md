```rust
use std::io::{Read, Write};
use std::net::{SocketAddr, TcpStream, ToSocketAddrs};
use std::time::Duration;

fn main() {
    let mut input = String::new();
    let _ = std::io::stdin().read_to_string(&mut input);
    let url = input.trim_end_matches(|c| c == '\n' || c == '\r');

    let output = match get_status_code(url) {
        Ok(code) => format!("{}\n", code),
        Err(_) => "error\n".to_string(),
    };

    let _ = std::io::stdout().write_all(output.as_bytes());
}

fn get_status_code(url: &str) -> Result<u16, ()> {
    let (host, port, path, host_header) = parse_http_url(url).ok_or(())?;

    let timeout = Duration::from_millis(5000);
    let mut last_err = None;

    // Resolve host to addresses
    let addrs_iter = (host.as_str(), port).to_socket_addrs().map_err(|e| {
        last_err.replace(e.to_string());
    });

    let addrs: Vec<SocketAddr> = match addrs_iter {
        Ok(iter) => iter.collect(),
        Err(_) => return Err(()),
    };

    if addrs.is_empty() {
        return Err(());
    }

    // Try to connect to one of the resolved addresses with timeout
    let mut stream_opt = None;
    for addr in addrs {
        match TcpStream::connect_timeout(&addr, timeout) {
            Ok(s) => {
                stream_opt = Some(s);
                break;
            }
            Err(e) => {
                last_err.replace(e.to_string());
                continue;
            }
        }
    }

    let mut stream = match stream_opt {
        Some(s) => s,
        None => return Err(()),
    };

    // Set read/write timeouts
    if stream.set_read_timeout(Some(timeout)).is_err() {
        return Err(());
    }
    if stream.set_write_timeout(Some(timeout)).is_err() {
        return Err(());
    }

    // Build and send request
    let req = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: 012-http-status-code/1\r\nAccept: */*\r\nConnection: close\r\n\r\n",
        path, host_header
    );
    if stream.write_all(req.as_bytes()).is_err() {
        return Err(());
    }

    // Read until first CRLF to get status line
    let mut buf = [0u8; 1024];
    let mut acc: Vec<u8> = Vec::with_capacity(1024);
    let status_line = loop {
        match stream.read(&mut buf) {
            Ok(0) => {
                // EOF before status line complete
                return Err(());
            }
            Ok(n) => {
                acc.extend_from_slice(&buf[..n]);
                if let Some(pos) = find_crlf(&acc) {
                    let line = &acc[..pos];
                    break String::from_utf8(line.to_vec()).map_err(|_| ())?;
                }
                // Continue reading
                if acc.len() > 8192 {
                    // Defensive: too much without CRLF
                    return Err(());
                }
            }
            Err(_) => return Err(()),
        }
    };

    parse_status_code(&status_line).ok_or(())
}

fn find_crlf(buf: &[u8]) -> Option<usize> {
    // Return the index of '\r' when "\r\n" is found
    if buf.len() < 2 {
        return None;
    }
    for i in 0..buf.len() - 1 {
        if buf[i] == b'\r' && buf[i + 1] == b'\n' {
            return Some(i);
        }
    }
    None
}

fn parse_status_code(status_line: &str) -> Option<u16> {
    // Expected: HTTP/1.1 200 OK
    let mut parts = status_line.split_whitespace();
    let proto = parts.next()?;
    if !proto.starts_with("HTTP/") {
        return None;
    }
    let code_str = parts.next()?;
    code_str.parse::<u16>().ok()
}

fn parse_http_url(url: &str) -> Option<(String, u16, String, String)> {
    // Returns (host_for_connect, port, path_and_query, host_header_value)
    let prefix = "http://";
    if !url.starts_with(prefix) {
        // Unsupported or invalid scheme
        return None;
    }
    let rest = &url[prefix.len()..];
    if rest.is_empty() {
        return None;
    }

    let (authority, path) = match rest.find('/') {
        Some(i) => (&rest[..i], &rest[i..]),
        None => (rest, "/"),
    };

    // Strip userinfo if present (use last '@' to handle emails in user)
    let hostport = match authority.rsplit_once('@') {
        Some((_userinfo, hostport)) => hostport,
        None => authority,
    };

    if hostport.is_empty() {
        return None;
    }

    let (host, port, host_header) = if hostport.starts_with('[') {
        // IPv6 literal
        let close = hostport.find(']')?;
        let host_inner = &hostport[1..close];
        if host_inner.is_empty() {
            return None;
        }
        let remainder = &hostport[close + 1..];
        let port = if remainder.is_empty() {
            80
        } else {
            if !remainder.starts_with(':') {
                return None;
            }
            remainder[1..].parse::<u16>().ok()?
        };
        let host_for_connect = host_inner.to_string();
        let mut host_header = String::new();
        host_header.push('[');
        host_header.push_str(host_inner);
        host_header.push(']');
        if port != 80 {
            host_header.push(':');
            host_header.push_str(&port.to_string());
        }
        (host_for_connect, port, host_header)
    } else {
        // Regular hostname or IPv4
        let (host_part, port_part_opt) = match hostport.rsplit_once(':') {
            Some((h, p)) if !p.is_empty() && p.chars().all(|c| c.is_ascii_digit()) => (h, Some(p)),
            _ => (hostport, None),
        };
        if host_part.is_empty() {
            return None;
        }
        let port = match port_part_opt {
            Some(p) => p.parse::<u16>().ok()?,
            None => 80,
        };
        let host_for_connect = host_part.to_string();
        let host_header = if port != 80 {
            format!("{}:{}", host_part, port)
        } else {
            host_part.to_string()
        };
        (host_for_connect, port, host_header)
    };

    let path = if path.is_empty() { "/" } else { path };

    Some((host, port, path.to_string(), host_header))
}
```