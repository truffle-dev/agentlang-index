```go
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	A, _ := reader.ReadString('\n')
	B, _ := reader.ReadString('\n')

	// Remove the newline characters
	A = A[:len(A)-1]
	B = B[:len(B)-1]

	fmt.Println(levenshteinDistance(A, B))
}

func levenshteinDistance(A, B string) int {
	lenA := len(A)
	lenB := len(B)

	// Create a 2D slice to store distances
	dp := make([][]int, lenA+1)
	for i := range dp {
		dp[i] = make([]int, lenB+1)
	}

	// Initialize the base cases
	for i := 0; i <= lenA; i++ {
		dp[i][0] = i
	}
	for j := 0; j <= lenB; j++ {
		dp[0][j] = j
	}

	// Fill the dp table
	for i := 1; i <= lenA; i++ {
		for j := 1; j <= lenB; j++ {
			if A[i-1] == B[j-1] {
				dp[i][j] = dp[i-1][j-1]
			} else {
				dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
			}
		}
	}

	return dp[lenA][lenB]
}

func min(a, b, c int) int {
	if a < b {
		if a < c {
			return a
		}
		return c
	}
	if b < c {
		return b
	}
	return c
}
```