```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"time"

	"bufio"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	url, _ := reader.ReadString('\n')
	aStr, _ := reader.ReadString('\n')
	bStr, _ := reader.ReadString('\n')

	url = url[:len(url)-1] // Trim newline
	aStr = aStr[:len(aStr)-1] // Trim newline
	bStr = bStr[:len(bStr)-1] // Trim newline

	a, err := strconv.Atoi(aStr)
	if err != nil {
		fmt.Print("error\n")
		return
	}

	b, err := strconv.Atoi(bStr)
	if err != nil {
		fmt.Print("error\n")
		return
	}

	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	body, err := json.Marshal(map[string]int{"a": a, "b": b})
	if err != nil {
		fmt.Print("error\n")
		return
	}

	resp, err := client.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		fmt.Print("error\n")
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Print("error\n")
		return
	}

	var result map[string]interface{}
	bodyBytes, _ := ioutil.ReadAll(resp.Body)
	if err := json.Unmarshal(bodyBytes, &result); err != nil {
		fmt.Print("error\n")
		return
	}

	sum, ok := result["sum"].(float64)
	if !ok {
		fmt.Print("error\n")
		return
	}

	fmt.Printf("%d\n", int(sum))
}
```