```go
package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	line, err := reader.ReadString('\n')
	if err != nil && err != io.EOF {
		w := bufio.NewWriter(os.Stdout)
		w.WriteString("error\n")
		w.Flush()
		return
	}
	url := strings.TrimRight(line, "\r\n")

	transport := &http.Transport{
		Proxy: nil,
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 30 * time.Second,
		}).DialContext,
		TLSHandshakeTimeout:   5 * time.Second,
		ExpectContinueTimeout: 1 * time.Second,
		ResponseHeaderTimeout: 5 * time.Second,
	}

	client := &http.Client{
		Timeout:   5 * time.Second,
		Transport: transport,
	}

	resp, err := client.Get(url)
	if err != nil {
		w := bufio.NewWriter(os.Stdout)
		w.WriteString("error\n")
		w.Flush()
		return
	}
	defer resp.Body.Close()

	w := bufio.NewWriter(os.Stdout)
	fmt.Fprintf(w, "%d\n", resp.StatusCode)
	w.Flush()
}
```