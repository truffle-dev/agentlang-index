```go
package main

import (
	"bufio"
	"net/http"
	"os"
	"strings"
	"time"
	"unicode"
)

func trimRightWS(s string) string {
	return strings.TrimRightFunc(s, unicode.IsSpace)
}

func writeError(w *bufio.Writer) {
	_, _ = w.WriteString("error\n")
	_ = w.Flush()
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	urlLine, err := in.ReadString('\n')
	if err != nil {
		writeError(out)
		return
	}
	hdrLine, err := in.ReadString('\n')
	if err != nil {
		writeError(out)
		return
	}

	urlStr := trimRightWS(urlLine)
	hdrName := trimRightWS(hdrLine)

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	req, err := http.NewRequest("GET", urlStr, nil)
	if err != nil {
		writeError(out)
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		writeError(out)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		writeError(out)
		return
	}

	key := http.CanonicalHeaderKey(hdrName)
	values, ok := resp.Header[key]
	if !ok || len(values) == 0 {
		writeError(out)
		return
	}

	_, _ = out.WriteString(values[0] + "\n")
}
```