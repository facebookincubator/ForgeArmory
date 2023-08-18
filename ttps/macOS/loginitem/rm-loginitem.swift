import Foundation
import Cocoa

print("Removing Calculator.app from login items...")

let temp = CFURLCreateFromFileSystemRepresentation(kCFAllocatorDefault, "/System/Applications/Calculator.app", "/System/Applications/Calculator.app".count, false)

var items = LSSharedFileListCreate(nil, kLSSharedFileListSessionLoginItems.takeUnretainedValue(), nil)?.takeUnretainedValue() as LSSharedFileList?

var cfName = CFStringCreateWithCString(nil, "Calculator.app", kCFStringEncodingASCII)

var loginItems = (LSSharedFileListCopySnapshot(items!, nil)?.takeRetainedValue())! as! Array<Any>

for each in loginItems{
    	if "\(each)".contains("Calculator.app"){
        	var result = LSSharedFileListItemRemove(items!, each as! LSSharedFileListItem)
        	print("[+] Clean-up completed: Calculator has been removed from Login Items")
        }
}



