```rust
use std::io::{self, Read, Write};
use std::net::TcpStream;
use std::time::Duration;

fn run() -> Result<String, ()> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).map_err(|_| ())?;
    
    let mut lines = input.lines();
    let url = lines.next().ok_or(())?.trim_end().to_string();
    let header_name = lines.next().ok_or(())?.trim_end().to_string();
    
    // Parse URL manually
    let url = url.trim();
    
    // Only support http://
    let rest = url.strip_prefix("http://").ok_or(())?;
    
    // Split host:port from path
    let (host_port, path) = if let Some(slash_pos) = rest.find('/') {
        (&rest[..slash_pos], &rest[slash_pos..])
    } else {
        (rest, "/")
    };
    
    let (host, port) = if let Some(colon_pos) = host_port.rfind(':') {
        let port: u16 = host_port[colon_pos+1..].parse().map_err(|_| ())?;
        (&host_port[..colon_pos], port)
    } else {
        (host_port, 80u16)
    };
    
    // Connect with timeout
    let addr = format!("{}:{}", host, port);
    
    // Resolve and connect
    use std::net::ToSocketAddrs;
    let mut addrs = addr.to_socket_addrs().map_err(|_| ())?;
    let sock_addr = addrs.next().ok_or(())?;
    
    let stream = TcpStream::connect_timeout(&sock_addr, Duration::from_millis(5000))
        .map_err(|_| ())?;
    stream.set_read_timeout(Some(Duration::from_millis(5000))).map_err(|_| ())?;
    stream.set_write_timeout(Some(Duration::from_millis(5000))).map_err(|_| ())?;
    
    // Send HTTP GET request
    let request = format!(
        "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n",
        path, host_port
    );
    
    let mut stream = stream;
    stream.write_all(request.as_bytes()).map_err(|_| ())?;
    
    // Read response
    let mut response = Vec::new();
    stream.read_to_end(&mut response).map_err(|_| ())?;
    
    // Parse response
    let response_str = String::from_utf8_lossy(&response);
    
    // Find header section end
    let header_end = response_str.find("\r\n\r\n").ok_or(())?;
    let headers_section = &response_str[..header_end];
    
    let mut header_lines = headers_section.lines();
    
    // Parse status line
    let status_line = header_lines.next().ok_or(())?;
    let status_code: u16 = status_line
        .split_whitespace()
        .nth(1)
        .ok_or(())?
        .parse()
        .map_err(|_| ())?;
    
    if status_code != 200 {
        return Err(());
    }
    
    // Find the requested header
    let header_name_lower = header_name.to_ascii_lowercase();
    
    for line in header_lines {
        if let Some(colon_pos) = line.find(':') {
            let name = &line[..colon_pos];
            let value = &line[colon_pos+1..];
            if name.to_ascii_lowercase() == header_name_lower {
                return Ok(value.trim().to_string());
            }
        }
    }
    
    Err(())
}

fn main() {
    let result = run();
    let output = match result {
        Ok(value) => format!("{}\n", value),
        Err(_) => "error\n".to_string(),
    };
    io::stdout().write_all(output.as_bytes()).unwrap();
}
```