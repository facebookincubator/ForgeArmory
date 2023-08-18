ObjC.import('sqlite3');
ObjC.import('Foundation');
app = Application.currentApplication();
app.includeStandardAdditions = true;

var user = $.NSUserName().js
var output = "";
var fileMan = $.NSFileManager.defaultManager;
var err;
var ffoxpath = '/Users/' + user + '/Library/Application\ Support/Firefox/Profiles';
if (fileMan.fileExistsAtPath(ffoxpath)){
	let prof_folders = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(ffoxpath,$()));
	try{
		for (p=0; p< prof_folders.length; p++){
			if ((prof_folders[p]).includes('-release')){
				var changeto = ffoxpath + "/" + prof_folders[p];
				var dircontents = ObjC.deepUnwrap(fileMan.contentsOfDirectoryAtPathError(changeto,$()));
				for (n=0; n<dircontents.length; n++){
					if (dircontents[n] == 'cookies.sqlite'){
						var ckpath = changeto + "/" + dircontents[n];
						var ppDb = Ref();
						var err = $.sqlite3_open(ckpath, ppDb)
						var db = ppDb[0]
						if(err != $.SQLITE_OK) throw new Error($.sqlite3_errmsg(db))
						var sql = 'select name,value,host,path,datetime(expiry,\'unixepoch\') as expiredate,isSecure,isHttpOnly,sameSite from moz_cookies'
						var ppStmt = Ref()
						var err = $.sqlite3_prepare(db, sql, -1, ppStmt, Ref())
						if(err != $.SQLITE_OK) throw new Error($.sqlite3_errmsg(db))
						pStmt = ppStmt[0]
						try{
                                                        output += 'FORMAT: cookie name | cookie value | host | path | expire date | isSecure | isHttpOnly | sameSite\n';
							output += '___________________________________________________________________________________________________\n';
							while((err = $.sqlite3_step(pStmt)) == $.SQLITE_ROW){
								output += $.sqlite3_column_text(pStmt,0) + " | " + $.sqlite3_column_text(pStmt,1) + " | " + $.sqlite3_column_text(pStmt,2) + " | " + $.sqlite3_column_text(pStmt,3) + " | " + $.sqlite3_column_text(pStmt,4) + " | " + $.sqlite3_column_text(pStmt,5) + " | " + $.sqlite3_column_text(pStmt,6) + " | " + $.sqlite3_column_text(pStmt,7) + " | \n"
							}
							output += '#####################################################################################################\n';
							console.log(output);
						}
						catch(error){
							output += error.toString()
							console.log(output);

						}
						//finally{
							//var err = $.sqlite3_finalize(pStmt)
							//var err = $.sqlite3_close(db)
							//if(err != $.SQLITE_OK) throw new Error($.sqlite3_errmsg(db))
						//}
					}



				}



			}
		}
	}

catch(err){
   console.log(err);
}

}
