import Foundation
import Cocoa
import SQLite3

let username = NSUserName()
var p1 = 0
var p2 = 0
var p3 = 0
var results = ""
var out = ""

//FDA Check
let dbpath = "/Users/\(username)/Library/Application Support/com.apple.TCC/TCC.db"
var db : OpaquePointer?
var dbURL = URL(fileURLWithPath: dbpath)
if sqlite3_open(dbURL.path, &db) != SQLITE_OK {
    print("##########################FDA Check###############################")
    print("[-] This app HAS NOT been grated full disk access - Cannot open the user's TCC db.")
    print("##################################################################")
    }
else {
    print("##########################FDA Check###############################")
    print("[+] This app HAS ALREADY been grated full disk access - Can open the user's TCC db")
    print("##################################################################")
}

results += "##########################TCC Folder Check###############################\n"
let queryString = "kMDItemKind = Folder -onlyin /Users/\(username)"
if let query = MDQueryCreate(kCFAllocatorDefault, queryString as CFString, nil, nil) {
    MDQueryExecute(query, CFOptionFlags(kMDQuerySynchronous.rawValue))

    for i in 0..<MDQueryGetResultCount(query) {
        if let rawPtr = MDQueryGetResultAtIndex(query, i) {
            let item = Unmanaged<MDItem>.fromOpaque(rawPtr).takeUnretainedValue()
            if let path = MDItemCopyAttribute(item, kMDItemPath) as? String {

                if path.hasSuffix("/Users/\(username)/Desktop"){
                    p1 = 1
                    results += "[+] This app HAS ALREADY been granted TCC access to \(path)\n"
                    results += "-----------------------------------------------------------------------------------\n"
                }
                if path.hasSuffix("/Users/\(username)/Documents"){
                    p2 = 1
                    results += "[+] This app HAS ALREADY been granted TCC access to \(path)\n"
                    results += "-----------------------------------------------------------------------------------\n"
                }
                if path.hasSuffix("/Users/\(username)/Downloads"){
                    p3 = 1
                    results += "[+] This app HAS ALREADY been granted TCC access to \(path)\n"
                    results += "-----------------------------------------------------------------------------------\n"
                }

            }
        }
    }

    if p1 == 0 {
        results += "[-] This app has NOT yet been given access to /Users/\(username)/Desktop. Be careful!!\n"
        results += "---------------------------------------------------------------\n"
    }

    if p2 == 0 {
        results += "[-] This app has NOT yet been given access to /Users/\(username)/Documents. Be careful!!\n"
        results += "---------------------------------------------------------------\n"
    }

    if p3 == 0 {
        results += "[-] This app has NOT yet been given access to /Users/\(username)/Downloads. Be careful!!\n"
        results += "---------------------------------------------------------------\n"
    }
}

print(results)
