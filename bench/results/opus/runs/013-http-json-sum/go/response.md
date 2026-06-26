```go
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net"
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
	aLine, _ := reader.ReadString('\n')
	bLine, _ := reader.ReadString('\n')

	url := strings.TrimSpace(urlLine)
	aStr := strings.TrimSpace(aLine)
	bStr := strings.TrimSpace(bLine)

	var a, b int
	if _, err := fmt.Sscanf(aStr, "%d", &a); err != nil {
		fmt.Fprintln(w, "error")
		return
	}
	if _, err := fmt.Sscanf(bStr, "%d", &b); err != nil {
		fmt.Fprintln(w, "error")
		return
	}

	body := fmt.Sprintf(`{"a":%d,"b":%d}`, a, b)

	client := &http.Client{
		Transport: &http.Transport{
			DialContext: (&net.Dialer{
				Timeout: 5000 * time.Millisecond,
			}).DialContext,
			TLSHandshakeTimeout:   5000 * time.Millisecond,
			ResponseHeaderTimeout: 5000 * time.Millisecond,
		},
		Timeout: 5000 * time.Millisecond,
	}

	resp, err := client.Post(url, "application/json", bytes.NewBufferString(body))
	if err != nil {
		fmt.Fprintln(w, "error")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Fprintln(w, "error")
		return
	}

	var result map[string]json.Number
	dec := json.NewDecoder(resp.Body)
	if err := dec.Decode(&result); err != nil {
		fmt.Fprintln(w, "error")
		return
	}

	sumVal, ok := result["sum"]
	if !ok {
		fmt.Fprintln(w, "error")
		return
	}

	n, err := sumVal.Int64()
	if err != nil {
		fmt.Fprintln(w, "error")
		return
	}

	fmt.Fprintln(w, n)
}
```