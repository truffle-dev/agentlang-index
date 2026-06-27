```go
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	readLine := func() (string, error) {
		line, err := reader.ReadString('\n')
		return strings.TrimRight(line, "\r\n \t"), err
	}

	fail := func() {
		fmt.Fprintln(writer, "error")
	}

	urlStr, err := readLine()
	if err != nil && urlStr == "" {
		fail()
		return
	}
	aStr, err := readLine()
	if err != nil && aStr == "" {
		fail()
		return
	}
	bStr, err := readLine()
	if err != nil && bStr == "" {
		fail()
		return
	}

	var a, b int32
	if _, err := fmt.Sscanf(strings.TrimSpace(aStr), "%d", &a); err != nil {
		fail()
		return
	}
	if _, err := fmt.Sscanf(strings.TrimSpace(bStr), "%d", &b); err != nil {
		fail()
		return
	}

	body := fmt.Sprintf(`{"a":%d,"b":%d}`, a, b)

	client := &http.Client{
		Timeout: 5000 * time.Millisecond,
	}

	resp, err := client.Post(urlStr, "application/json", bytes.NewBufferString(body))
	if err != nil {
		fail()
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fail()
		return
	}

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fail()
		return
	}

	var result map[string]interface{}
	if err := json.Unmarshal(respBody, &result); err != nil {
		fail()
		return
	}

	sumVal, ok := result["sum"]
	if !ok {
		fail()
		return
	}

	sumFloat, ok := sumVal.(float64)
	if !ok {
		fail()
		return
	}

	sum := int32(sumFloat)
	if float64(sum) != sumFloat {
		fail()
		return
	}

	fmt.Fprintln(writer, sum)
}
```