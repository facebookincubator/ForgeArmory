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

ObjC.import('sqlite3');
ObjC.import('Foundation');

app = Application.currentApplication();
app.includeStandardAdditions = true;

var user = $.NSUserName().js;
var output = "";
var fileMan = $.NSFileManager.defaultManager;
var err;
var ffoxpath = '/Users/' + user + '/Library/Application Support/Firefox/Profiles';

if (fileMan.fileExistsAtPath(ffoxpath)) {
    console.log("Found Firefox directory at " + ffoxpath);
    let prof_folders = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(ffoxpath, $()));
    console.log("Profile folders found: " + prof_folders.length);
    try {
        for (p = 0; p < prof_folders.length; p++) {
            if (prof_folders[p].includes('-release')) {
                var changeto = ffoxpath + "/" + prof_folders[p];
                var dircontents = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(changeto, $()));
                for (n = 0; n < dircontents.length; n++) {
                    if (dircontents[n] == 'cookies.sqlite') {
                        var ckpath = changeto + "/" + dircontents[n];
                        var ppDb = Ref();
                        err = $.sqlite3_open(ckpath, ppDb);
                        var db = ppDb[0];
                        if (err != $.SQLITE_OK) {
                            throw new Error($.sqlite3_errmsg(db));
                        }
                        var sql = 'select name,value,host,path,datetime(expiry,\'unixepoch\') as expiredate,isSecure,isHttpOnly,sameSite from moz_cookies';
                        var ppStmt = Ref();
                        err = $.sqlite3_prepare(db, sql, -1, ppStmt, Ref());
                        if (err != $.SQLITE_OK) {
                            throw new Error($.sqlite3_errmsg(db));
                        }
                        pStmt = ppStmt[0];
                        try {
                            output += 'FORMAT: cookie name | cookie value | host | path | expire date | isSecure | isHttpOnly | sameSite\n';
                            output += '___________________________________________________________________________________________________\n';
                            while ((err = $.sqlite3_step(pStmt)) == $.SQLITE_ROW) {
                                output += $.sqlite3_column_text(pStmt, 0) + " | " +
                                          $.sqlite3_column_text(pStmt, 1) + " | " +
                                          $.sqlite3_column_text(pStmt, 2) + " | " +
                                          $.sqlite3_column_text(pStmt, 3) + " | " +
                                          $.sqlite3_column_text(pStmt, 4) + " | " +
                                          $.sqlite3_column_text(pStmt, 5) + " | " +
                                          $.sqlite3_column_text(pStmt, 6) + " | " +
                                          $.sqlite3_column_text(pStmt, 7) + " |\n";
                            }
                            output += '#####################################################################################################\n';
                            console.log(output);
                        } catch (error) {
                            output += error.toString();
                            console.log(output);
                        }
                    }
                }
            }
        }
    } catch (err) {
        console.log(err);
    }
}

// Print all the cookies at the end
console.log(output);
