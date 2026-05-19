```zero
use std::net
use std::json
use std::buf
use std::time

fn main() {
    let args = std.args()
    if args.len() != 4 {
        check world.out.write("error\n")
        return
    }

    let url = args[1]
    let a_str = args[2]
    let b_str = args[3]

    let a = match std.parse::int32(a_str.trim()) {
        Some(val) => val,
        None => {
            check world.out.write("error\n")
            return
        }
    }

    let b = match std.parse::int32(b_str.trim()) {
        Some(val) => val,
        None => {
            check world.out.write("error\n")
            return
        }
    }

    let json_body = "{\"a\":".as_bytes() + a_str.trim().as_bytes() + ",\"b\":".as_bytes() + b_str.trim().as_bytes() + "}".as_bytes()

    let timeout = time::Duration::from_millis(5000)
    let request = net::http::Request::post(url, json_body)
        .header("Content-Type", "application/json")
        .timeout(timeout)

    let response = match request.send() {
        Ok(resp) => resp,
        Err(_) => {
            check world.out.write("error\n")
            return
        }
    }

    if response.status() != 200 {
        check world.out.write("error\n")
        return
    }

    let body = match response.body() {
        Ok(b) => b,
        Err(_) => {
            check world.out.write("error\n")
            return
        }
    }

    let json_obj = match json::parse(body) {
        Ok(obj) => obj,
        Err(_) => {
            check world.out.write("error\n")
            return
        }
    }

    let sum = match json_obj.get("sum") {
        Some(json::Value::Int(s)) => s,
        _ => {
            check world.out.write("error\n")
            return
        }
    }

    let mut buf = buf::Array::<u8, 32>::new()
    let n = match std.fmt::itoa(buf.as_mut(), sum) {
        Some(len) => len,
        None => {
            check world.out.write("error\n")
            return
        }
    }

    check world.out.write(buf[0..n])
    check world.out.write("\n")
    return
}
```