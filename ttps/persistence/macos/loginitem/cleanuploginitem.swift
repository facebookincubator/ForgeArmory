import Foundation
import Cocoa

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

        if let actualURL = resolvedURL?.takeRetainedValue() as URL? {

            if actualURL.path == path {

                let result = LSSharedFileListItemRemove(items, item)
                if result == noErr {
                    print("[+] Cleanup: \(path) has been removed from Login Items")
                } else {
                    print("[-] Error removing \(path) from Login Items")
                }
            }
        }
    }

    // If the default path, remove the file
    if path == "/Users/Shared/calc.sh" {
        removeFile(atPath: path)
    }
}

// Remove a file from the filesystem
func removeFile(atPath path: String) {
    do {
        try FileManager.default.removeItem(atPath: path)
        print("[+] Successfully removed file at: \(path)")
    } catch {
        print("[-] Failed to remove file at: \(path). Error: \(error)")
    }
}

// Check if we have the necessary argument
guard CommandLine.arguments.count > 1 else {
    print("[!] Missing parameters. Usage: programName <path>")
    exit(1)
}

let commandOrPath = CommandLine.arguments[1]

// Start cleanup
cleanupLoginItem(withPath: commandOrPath)
