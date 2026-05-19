```zero
use lib http

fn main() {
    url := std.args[1].trim()
    header_name := std.args[2].trim().to_lowercase()

    response := check http.get(url, 5000)
    if response.status != 200 {
        check world.out.write("error\n")
        return
    }

    for header in response.headers {
        if header.name.to_lowercase() == header_name {
            check world.out.write(header.value)
            check world.out.write("\n")
            return
        }
    }

    check world.out.write("error\n")
    return
}
```