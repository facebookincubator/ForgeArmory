/*
Copyright © 2023-present, Meta Platforms, Inc. and affiliates
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// @nolint
//go:build ignore

package main

import (
	"encoding/hex"
	"fmt"
	"net/http"
	"os"
	"strings"
)

func main() {
	handler := http.HandlerFunc(handleRequest)
	http.Handle("/", handler)
	http.ListenAndServe("0.0.0.0:80", nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {

	uri := r.URL.String()
	fmt.Println(uri)
	uri2 := strings.Replace(uri, "/", "", 1)
	decoded, _ := hex.DecodeString(uri2)

	p, perr := os.OpenFile("outfile",
		os.O_WRONLY|os.O_APPEND|os.O_CREATE,
		0666)
	if perr != nil {
		fmt.Println("[-] Error creating the outfile...")
	}
	defer p.Close()

	p.Write(decoded)

}
