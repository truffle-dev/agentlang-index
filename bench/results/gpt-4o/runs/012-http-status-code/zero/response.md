```zero
use std::net
use std::http
use std::result
use std::string
use std::option
use std::time

export fn main() {
    let args = std.args()
    if args.len() < 2 {
        check world.out.write("error\n")
        return
    }

    let url = args[1]
    let trimmed_url = string.trim(url)

    let timeout = time.Duration::from_millis(5000)
    let request_result = http.get(trimmed_url, timeout)

    match request_result {
        result.Ok(response) => {
            let status_code = response.status_code()
            let status_str = string.from_int(status_code)
            check world.out.write(status_str)
            check world.out.write("\n")
        }
        result.Err(_) => {
            check world.out.write("error\n")
        }
    }
}
```