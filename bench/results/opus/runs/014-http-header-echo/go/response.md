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
	w := bufio.NewWriter(os.Stdout)
	defer w.Flush()

	urlLine, _ := reader.ReadString('\n')
	headerLine, _ := reader.ReadString('\n')

	url := strings.TrimRight(urlLine, " \t\r\n")
	headerName := strings.TrimRight(headerLine, " \t\r\n")

	client := &http.Client{Timeout: 5000 * time.Millisecond}
	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintln(w, "error")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Fprintln(w, "error")
		return
	}

	val := resp.Header.Get(headerName)
	if val == "" {
		fmt.Fprintln(w, "error")
		return
	}

	fmt.Fprintln(w, val)
}
```