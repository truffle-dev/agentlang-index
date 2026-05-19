```zero
use lib http

fn main() {
    url := std.args[1].trim()
    response := http.get(url, 5000)
    match response {
        Ok(res) => {
            check world.out.write(res.status_code.to_string() + "\n")
        }
        Err(_) => {
            check world.out.write("error\n")
        }
    }
    return
}
```