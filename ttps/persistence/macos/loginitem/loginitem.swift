import Foundation
import Cocoa
import OSAKit

// Function for Cleanup
func cleanupLoginItem(withPath path: String) {
    print("Removing \(path) from login items...")

    guard let items = LSSharedFileListCreate(nil, kLSSharedFileListSessionLoginItems.takeUnretainedValue(), nil)?.takeUnretainedValue() else {
        print("[-] Could not obtain the list of Login Items.")
        return
    }

    guard let loginItems = LSSharedFileListCopySnapshot(items, nil)?.takeRetainedValue() as? [LSSharedFileListItem] else {
        print("[-] Could not copy the snapshot of Login Items.")
        return
    }

    for item in loginItems {
    var resolvedURL: Unmanaged<CFURL>?
    LSSharedFileListItemResolve(item, 0, &resolvedURL, nil)
    if let actualURL = resolvedURL?.takeRetainedValue() as URL?, actualURL.path == path {
        if CFURLGetString(actualURL as CFURL) as String == path {
            let result = LSSharedFileListItemRemove(items, item)
            if result == noErr {
                print("[+] Cleanup: \(path) has been removed from Login Items")
            } else {
                print("[-] Error removing \(path) from Login Items")
            }
        }
    }
}

}

// Remove a file from the filesystem
func removeFile(atPath path: String) {
    do {
        try FileManager.default.removeItem(atPath: path)
        print("[+] Successfully removed file at: \(path)")
    } catch {
        print("[-] Failed to remove file at: \(path)")
    }
}

// Main Execution
print("This TTP will add the provided path or shell command to Login Items. If cleanup is true, it will then remove it.")

// Check if we have the necessary argument
guard CommandLine.arguments.count > 2 else {
    print("[!] Missing parameters. Usage: programName <path> <true|false>")
    exit(1)
}

let commandOrPath = CommandLine.arguments[1]
let cleanupAction = CommandLine.arguments[2].lowercased()

// Check for default /Users/Shared/calc.sh behavior
if commandOrPath == "/Users/Shared/calc.sh" {
    let script = """
    #!/bin/bash
    open -a Calculator.app
    """

    let fileMan = FileManager.default
    let scriptData = Data(script.utf8)
    try? fileMan.createFile(atPath: commandOrPath, contents: scriptData, attributes: nil)

    var attributes = [FileAttributeKey: Any]()
    attributes[.posixPermissions] = 0o755
    try? fileMan.setAttributes(attributes, ofItemAtPath: commandOrPath)
}

// Always add to login items first
print(" ===> Attempting to create Login Item persistence")
do {
    let jxa = """
    ObjC.import('CoreServices');
    ObjC.import('Security');
    ObjC.import('SystemConfiguration');
    let temp = $.CFURLCreateFromFileSystemRepresentation($.kCFAllocatorDefault, "\(commandOrPath)", "\(commandOrPath)".length, false);
    let items = $.LSSharedFileListCreate($.kCFAllocatorDefault, $.kLSSharedFileListSessionLoginItems, $.nil);
    let cfName = $.CFStringCreateWithCString($.nil, "\(commandOrPath)", $.kCFStringEncodingASCII);
    let itemRef = $.LSSharedFileListInsertItemURL(items, $.kLSSharedFileListItemLast, cfName, $.nil, temp, $.nil, $.nil);
    console.log("[+] \(commandOrPath) successfully added as a Login Item");
    """

    let script = OSAScript.init(source: jxa, language: OSALanguage.init(forName: "JavaScript"))
    var compileErr : NSDictionary?
    script.executeAndReturnError(&compileErr)
    var scriptErr : NSDictionary?
    script.executeAndReturnError(&scriptErr)

    print("[+] \(commandOrPath) successfully added as a Login Item")
} catch let error {
    print("[-] Error: \(error)")
}

// If cleanup flag is true, remove the item from login items
if cleanupAction == "true" {
    cleanupLoginItem(withPath: commandOrPath)

    // If it's the default calc script, remove it
    if commandOrPath == "/Users/Shared/calc.sh" {
        removeFile(atPath: commandOrPath)
    }
}
