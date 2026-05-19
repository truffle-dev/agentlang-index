```go
package main

import (
	"bufio"
	"encoding/json"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	fail := func() {
		out.WriteString("error\n")
		out.Flush()
	}

	readLine := func() (string, error) {
		s, err := in.ReadString('\n')
		if err != nil {
			return "", err
		}
		return strings.TrimRight(s, "\r\n"), nil
	}

	urlStr, err := readLine()
	if err != nil {
		fail()
		return
	}
	aLine, err := readLine()
	if err != nil {
		fail()
		return
	}
	bLine, err := readLine()
	if err != nil {
		fail()
		return
	}

	aStr := strings.TrimSpace(aLine)
	bStr := strings.TrimSpace(bLine)

	a64, err := strconv.ParseInt(aStr, 10, 32)
	if err != nil {
		fail()
		return
	}
	b64, err := strconv.ParseInt(bStr, 10, 32)
	if err != nil {
		fail()
		return
	}

	body := `{"a":` + strconv.FormatInt(a64, 10) + `,"b":` + strconv.FormatInt(b64, 10) + `}`

	tr := &http.Transport{
		Proxy: http.ProxyFromEnvironment,
		DialContext: (&net.Dialer{
			Timeout: 5 * time.Second,
		}).DialContext,
		TLSHandshakeTimeout:   5 * time.Second,
		ResponseHeaderTimeout: 5 * time.Second,
		ExpectContinueTimeout: 1 * time.Second,
	}
	client := &http.Client{
		Transport: tr,
		Timeout:   5 * time.Second,
	}

	req, err := http.NewRequest("POST", urlStr, strings.NewReader(body))
	if err != nil {
		fail()
		return
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		fail()
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fail()
		return
	}

	dec := json.NewDecoder(resp.Body)
	dec.UseNumber()
	var m map[string]any
	if err := dec.Decode(&m); err != nil {
		fail()
		return
	}

	val, ok := m["sum"]
	if !ok {
		fail()
		return
	}
	num, ok := val.(json.Number)
	if !ok {
		fail()
		return
	}
	i64, err := num.Int64()
	if err != nil {
		fail()
		return
	}

	out.WriteString(strconv.FormatInt(i64, 10))
	out.WriteByte('\n')
}
```