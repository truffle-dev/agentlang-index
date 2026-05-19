```rust
use std::io::{Read, Write};
use std::net::{TcpStream, ToSocketAddrs};
use std::time::Duration;

struct ParsedUrl {
    host_connect: String, // host without brackets
    host_header: String,  // host as to be used in Host header (with brackets for IPv6, and port if non-default)
    port: u16,
    path: String,
}

fn parse_url(url: &str) -> Result<ParsedUrl, ()> {
    let rest = if let Some(r) = url.strip_prefix("http://") {
        r
    } else {
        // unsupported or malformed
        return Err(());
    };

    // Split into authority and path
    let mut parts = rest.splitn(2, '/');
    let authority = parts.next().ok_or(())?;
    if authority.is_empty() {
        return Err(());
    }
    let mut path = match parts.next() {
        Some(p) => format!("/{}", p),
        None => "/".to_string(),
    };
    // strip fragment if any
    if let Some(hash_idx) = path.find('#') {
        path.truncate(hash_idx);
    }

    // Reject userinfo if present
    if authority.contains('@') {
        return Err(());
    }

    let (host_connect, host_header_base, port) = if authority.starts_with('[') {
        // IPv6 literal
        let end = authority.find(']').ok_or(())?;
        let inside = &authority[1..end];
        let remainder = &authority[end + 1..];
        let mut port: u16 = 80;
        if remainder.is_empty() {
            // ok
        } else if let Some(rest) = remainder.strip_prefix(':') {
            port = rest.parse::<u16>().map_err(|_| ())?;
        } else {
            // unexpected characters after ]
            return Err(());
        }
        let host_connect = inside.to_string();
        let host_header_base = format!("[{}]", inside);
        (host_connect, host_header_base, port)
    } else {
        // IPv4 or hostname
        let mut host = authority;
        let mut port: u16 = 80;
        if let Some(colon_idx) = authority.rfind(':') {
            // If there is a colon, it might be a port. Since no brackets, treat last colon as port separator.
            let (h, pstr) = authority.split_at(colon_idx);
            if !pstr.is_empty() {
                let pstr = &pstr[1..];
                if !pstr.is_empty() {
                    port = pstr.parse::<u16>().map_err(|_| ())?;
                    host = h;
                }
            }
        }
        if host.is_empty() {
            return Err(());
        }
        (host.to_string(), host.to_string(), port)
    };

    let host_header = if port != 80 {
        format!("{}:{}", host_header_base, port)
    } else {
        host_header_base
    };

    Ok(ParsedUrl {
        host_connect,
        host_header,
        port,
        path,
    })
}

fn find_header_end(buf: &[u8]) -> Option<usize> {
    buf.windows(4).position(|w| w == b"\r\n\r\n")
}

fn main() {
    // Always exit 0; write only to stdout
    let mut input = String::new();
    if std::io::stdin().read_to_string(&mut input).is_err() {
        let _ = std::io::stdout().write_all(b"error\n");
        return;
    }

    let mut it = input.lines();
    let url_line = match it.next() {
        Some(s) => s.trim_end(),
        None => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };
    let header_line = match it.next() {
        Some(s) => s.trim_end(),
        None => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };

    if url_line.is_empty() || header_line.is_empty() {
        let _ = std::io::stdout().write_all(b"error\n");
        return;
    }

    let header_name_lower = header_line.to_ascii_lowercase();

    let parsed = match parse_url(url_line) {
        Ok(p) => p,
        Err(_) => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };

    // Resolve and connect with timeout
    let timeout = Duration::from_millis(5000);
    let mut addrs_iter = match (parsed.host_connect.as_str(), parsed.port).to_socket_addrs() {
        Ok(it) => it,
        Err(_) => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };

    let mut stream_opt: Option<TcpStream> = None;
    for addr in addrs_iter.by_ref() {
        match TcpStream::connect_timeout(&addr, timeout) {
            Ok(s) => {
                stream_opt = Some(s);
                break;
            }
            Err(_) => continue,
        }
    }

    let mut stream = match stream_opt {
        Some(s) => s,
        None => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };

    let _ = stream.set_read_timeout(Some(timeout));
    let _ = stream.set_write_timeout(Some(timeout));

    // Build and send request
    let request = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n",
        parsed.path, parsed.host_header
    );

    if stream.write_all(request.as_bytes()).is_err() {
        let _ = std::io::stdout().write_all(b"error\n");
        return;
    }

    // Read until headers end
    let mut buf: Vec<u8> = Vec::with_capacity(1024);
    let mut tmp = [0u8; 1024];
    let header_end_pos: usize;
    loop {
        match stream.read(&mut tmp) {
            Ok(0) => {
                // EOF before headers complete
                let _ = std::io::stdout().write_all(b"error\n");
                return;
            }
            Ok(n) => {
                buf.extend_from_slice(&tmp[..n]);
                if let Some(pos) = find_header_end(&buf) {
                    header_end_pos = pos;
                    break;
                }
            }
            Err(_) => {
                let _ = std::io::stdout().write_all(b"error\n");
                return;
            }
        }
    }

    let headers_bytes = &buf[..header_end_pos];
    // Parse status line
    let mut lines_iter = headers_bytes.split(|&b| b == b'\r').peekable();

    let status_line = match lines_iter.next() {
        Some(line_prefix) => {
            // status line should be followed by '\n', but split_by '\r' keeps before; it's ok
            // Remove trailing '\n' if present next char
            let mut line = line_prefix.to_vec();
            // If next byte after status_line is '\n', it's in the following split piece (empty before '\n'), but our splitting by '\r' doesn't include '\n'
            line
        }
        None => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };
    // status_line currently includes bytes before first '\r'; might include trailing '\n' if server used only '\n', unlikely. Let's trim trailing '\n' if exists.
    let status_line = if let Some(&b'\n') = status_line.last() {
        &status_line[..status_line.len() - 1]
    } else {
        &status_line[..]
    };

    // Convert status line to parse code
    let status_str = String::from_utf8_lossy(status_line);
    let mut status_parts = status_str.split_whitespace();
    let _httpver = status_parts.next().unwrap_or("");
    let code_str = status_parts.next().unwrap_or("");
    let code: u16 = match code_str.parse::<u16>() {
        Ok(c) => c,
        Err(_) => {
            let _ = std::io::stdout().write_all(b"error\n");
            return;
        }
    };
    if code != 200 {
        let _ = std::io::stdout().write_all(b"error\n");
        return;
    }

    // Iterate over remaining header lines
    // Reconstruct lines reliably by splitting on CRLF
    let mut found_value: Option<Vec<u8>> = None;
    // Split full headers_bytes into lines by CRLF
    let mut start = 0usize;
    while start < headers_bytes.len() {
        // find next CRLF
        let mut end = None;
        let mut i = start;
        while i + 1 < headers_bytes.len() {
            if headers_bytes[i] == b'\r' && headers_bytes[i + 1] == b'\n' {
                end = Some(i);
                break;
            }
            i += 1;
        }
        let line_end = match end {
            Some(e) => e,
            None => headers_bytes.len(),
        };

        // Extract line
        if line_end > start {
            let line = &headers_bytes[start..line_end];
            // Skip status line (first line). We already consumed but for safety:
            // Detect presence of colon
            if let Some(colon_idx) = line.iter().position(|&b| b == b':') {
                let (name_bytes, value_bytes_full) = line.split_at(colon_idx);
                let mut value_bytes = &value_bytes_full[1..]; // skip ':'
                // trim leading SP/HTAB
                while let Some(&b) = value_bytes.first() {
                    if b == b' ' || b == b'\t' {
                        value_bytes = &value_bytes[1..];
                    } else {
                        break;
                    }
                }
                // Compare header name ASCII case-insensitive
                if name_bytes.len() == header_name_lower.len() {
                    let mut eq = true;
                    for (i, &nb) in name_bytes.iter().enumerate() {
                        if nb.to_ascii_lowercase() != header_name_lower.as_bytes()[i] {
                            eq = false;
                            break;
                        }
                    }
                    if eq {
                        found_value = Some(value_bytes.to_vec());
                        break;
                    }
                } else {
                    // lengths differ; still need to check ignoring case but with different lengths can't be equal
                }
            }
        }

        // Move to next line after CRLF
        if let Some(e) = end {
            start = e + 2;
        } else {
            break;
        }
    }

    match found_value {
        Some(mut v) => {
            // Write value followed by newline
            v.push(b'\n');
            let _ = std::io::stdout().write_all(&v);
        }
        None => {
            let _ = std::io::stdout().write_all(b"error\n");
        }
    }
}
```