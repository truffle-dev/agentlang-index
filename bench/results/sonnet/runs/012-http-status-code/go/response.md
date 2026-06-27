```go
package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	line, _ := reader.ReadString('\n')
	url := strings.TrimRight(line, "\r\n")

	client := &http.Client{
		Timeout: 5000 * time.Millisecond,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintln(writer, "error")
		return
	}
	defer resp.Body.Close()

	fmt.Fprintln(writer, resp.StatusCode)
}
```