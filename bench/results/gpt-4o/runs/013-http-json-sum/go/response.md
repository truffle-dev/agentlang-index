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
	"strconv"
	"strings"
	"time"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	url, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("error")
		return
	}
	url = strings.TrimSpace(url)

	aStr, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("error")
		return
	}
	aStr = strings.TrimSpace(aStr)

	bStr, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("error")
		return
	}
	bStr = strings.TrimSpace(bStr)

	a, err := strconv.Atoi(aStr)
	if err != nil {
		fmt.Println("error")
		return
	}

	b, err := strconv.Atoi(bStr)
	if err != nil {
		fmt.Println("error")
		return
	}

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	requestBody, err := json.Marshal(map[string]int{"a": a, "b": b})
	if err != nil {
		fmt.Println("error")
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("error")
		return
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("error")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Println("error")
		return
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("error")
		return
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		fmt.Println("error")
		return
	}

	sum, ok := result["sum"].(float64)
	if !ok {
		fmt.Println("error")
		return
	}

	fmt.Printf("%d\n", int(sum))
}
```