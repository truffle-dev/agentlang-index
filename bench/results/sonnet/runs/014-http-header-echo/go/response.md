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

	urlLine, _ := reader.ReadString('\n')
	headerLine, _ := reader.ReadString('\n')

	url := strings.TrimRight(urlLine, "\r\n \t")
	headerName := strings.TrimRight(headerLine, "\r\n \t")

	client := &http.Client{
		Timeout: 5000 * time.Millisecond,
	}

	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintln(writer, "error")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Fprintln(writer, "error")
		return
	}

	val := resp.Header.Get(headerName)
	if val == "" {
		fmt.Fprintln(writer, "error")
		return
	}

	fmt.Fprintln(writer, val)
}
```