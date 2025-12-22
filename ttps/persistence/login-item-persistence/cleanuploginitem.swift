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
        var error: Unmanaged<CFError>? = nil
        resolvedURL = LSSharedFileListItemCopyResolvedURL(item, 0, &error)

        if let actualURL = resolvedURL?.takeRetainedValue() as URL? {

            if actualURL.path == path {
                // Deprecated function, we may need to
                // consider alternatives in the future.
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
