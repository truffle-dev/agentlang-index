```zero
use lib http
use lib json
use lib std

fn main() {
    url := std.args[1]
    a := std.args[2].parseInt()
    b := std.args[3].parseInt()
    body := json.stringify({"a": a, "b": b})
    headers := {"Content-Type": "application/json"}
    response := http.post(url, body, headers, 5000)

    match response {
        .success(resp) {
            if resp.status == 200 {
                result := json.parse(resp.body)
                match result {
                    .object(obj) {
                        if obj.has("sum") {
                            sum := obj.get("sum").asInt()
                            check std.world.out.write(sum.toString() + "\n")
                            return
                        }
                    }
                    .error(_) {}
                }
            }
        }
        .error(_) {}
    }
    check std.world.out.write("error\n")
    return
}
```