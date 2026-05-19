```zero
use http
use option
use result
use string
use vec

fn main() {
    let args = std.args
    if args.len() != 3 {
        check world.out.write("error\n")
        return
    }

    let url = string.trim(args[1])
    let header_name = string.trim(args[2])

    let client = http.client()
    client.set_timeout(5000)

    let response_result = client.get(url)
    if result.is_err(response_result) {
        check world.out.write("error\n")
        return
    }

    let response = result.unwrap(response_result)
    if response.status_code != 200 {
        check world.out.write("error\n")
        return
    }

    let headers = response.headers
    let header_value_option = headers.get(header_name, true) // true for case-insensitive

    if option.is_none(header_value_option) {
        check world.out.write("error\n")
        return
    }

    let header_value = option.unwrap(header_value_option)
    check world.out.write(header_value)
    check world.out.write("\n")
    return
}
```