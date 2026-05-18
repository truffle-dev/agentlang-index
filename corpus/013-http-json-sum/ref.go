// HTTP POST + JSON sum reference for AgentLang Index.

package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

func fail() {
	fmt.Print("error\n")
}

func run() bool {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 0, 4096), 1<<20)
	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
		if len(lines) == 3 {
			break
		}
	}
	if len(lines) < 3 {
		return false
	}
	url := strings.TrimSpace(lines[0])
	a, err := strconv.Atoi(strings.TrimSpace(lines[1]))
	if err != nil {
		return false
	}
	b, err := strconv.Atoi(strings.TrimSpace(lines[2]))
	if err != nil {
		return false
	}
	if url == "" {
		return false
	}

	body := []byte(fmt.Sprintf(`{"a":%d,"b":%d}`, a, b))
	req, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(body))
	if err != nil {
		return false
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{
		Timeout: 5 * time.Second,
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return false
	}

	var parsed map[string]json.RawMessage
	dec := json.NewDecoder(resp.Body)
	if err := dec.Decode(&parsed); err != nil {
		return false
	}
	rawSum, ok := parsed["sum"]
	if !ok {
		return false
	}
	var n json.Number
	if err := json.Unmarshal(rawSum, &n); err != nil {
		return false
	}
	s, err := n.Int64()
	if err != nil {
		return false
	}
	fmt.Printf("%d\n", s)
	return true
}

func main() {
	if !run() {
		fail()
	}
}
