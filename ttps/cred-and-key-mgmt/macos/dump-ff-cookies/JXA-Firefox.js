ObjC.import('sqlite3');
ObjC.import('Foundation');

app = Application.currentApplication();
app.includeStandardAdditions = true;

var user = $.NSUserName().js;
var allCookiesOutput = ""; // Change here
var fileMan = $.NSFileManager.defaultManager;
var ffoxpath = '/Users/' + user + '/Library/Application Support/Firefox/Profiles';

if (fileMan.fileExistsAtPath(ffoxpath)) {
    console.log("Found Firefox directory at " + ffoxpath);
    let prof_folders = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(ffoxpath, $()));
    console.log("Profile folders found: " + prof_folders.length);

    try {
        for (var p = 0; p < prof_folders.length; p++) {
            var changeto = ffoxpath + "/" + prof_folders[p];
            console.log("Checking profile folder: " + prof_folders[p]);
            var dircontents = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(changeto, $()));

            for (var n = 0; n < dircontents.length; n++) {
                if (dircontents[n] == 'cookies.sqlite') {
                    var ckpath = changeto + "/" + dircontents[n];
                    var ppDb = Ref();
                    var err = $.sqlite3_open(ckpath, ppDb);
                    var db = ppDb[0];
                    if (err != $.SQLITE_OK) {
                        console.log("Error opening database: " + $.sqlite3_errmsg(db));
                        throw new Error($.sqlite3_errmsg(db));
                    }

                    var sql = 'select name,value,host,path,datetime(expiry,\'unixepoch\') as expiredate,isSecure,isHttpOnly from moz_cookies';
                    var ppStmt = Ref();
                    var err = $.sqlite3_prepare(db, sql, -1, ppStmt, Ref());
                    if (err != $.SQLITE_OK) {
                        console.log("Error preparing statement: " + $.sqlite3_errmsg(db));
                        throw new Error($.sqlite3_errmsg(db));
                    }
                    var pStmt = ppStmt[0];

                    try {
                        allCookiesOutput += 'Profile folder: ' + prof_folders[p] + '\n'; // Change here
                        allCookiesOutput += 'FORMAT: cookie name | cookie value | host | path | expire date | isSecure | isHttpOnly\n'; // Change here
                        allCookiesOutput += '___________________________________________________________________________________________________\n'; // Change here

                        var stepResult;
                        while ((stepResult = $.sqlite3_step(pStmt)) == $.SQLITE_ROW) {
                            var name = $.sqlite3_column_text(pStmt, 0);
                            var value = $.sqlite3_column_text(pStmt, 1);
                            var host = $.sqlite3_column_text(pStmt, 2);
                            var path = $.sqlite3_column_text(pStmt, 3);
                            var expiredate = $.sqlite3_column_text(pStmt, 4);
                            var isSecure = $.sqlite3_column_text(pStmt, 5);
                            var isHttpOnly = $.sqlite3_column_text(pStmt, 6);

                            allCookiesOutput += name + " | " + value + " | " + host + " | " + path + " | " + expiredate + " | " + isSecure + " | " + isHttpOnly + "\n"; // Change here
                        }

                        if (stepResult != $.SQLITE_DONE) {
                            console.log("Error executing statement: " + $.sqlite3_errmsg(db));
                        }

                    } catch (error) {
                        console.log("Error processing results: " + error.toString());
                    } finally {
                        $.sqlite3_finalize(pStmt);
                        $.sqlite3_close(db);
                    }
                }

            }
        }
    } catch (err) {
        console.log(err);
    }
}

// Print all the cookies at the end
console.log(allCookiesOutput);
