// @nolint
import Foundation
import Cocoa

let pasteboard = NSPasteboard.general
pasteboard.clearContents()
pasteboard.setString("AnotherSecretClipboardString", forType: .string)
let pString = pasteboard.string(forType: .string)!

if pString.contains("AnotherSecretClipboardString"){
        print("[+] TTP successfully completed! String dumped from the clipboard: " + pString)
}
else {
        print("[-] TTP did not successfully complete. Exiting...")
}
