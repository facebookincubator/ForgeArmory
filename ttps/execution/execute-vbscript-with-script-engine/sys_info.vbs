Set objWMIService = GetObject( "winmgmts:\\.\root\cimv2" )
Set objList = objWMIService.ExecQuery( "Select * from Win32_ComputerSystem" )

For Each objItem in objList
        strDomain = objItem.Domain
	strName = objItem.Name
	strManu = objItem.Manufacturer
	strModel = objItem.Model

	output = "Domain: " & strDomain & vbNewLine & _
       		 "Computer Name: " & strName & vbNewLine & _
			 "Manufacturer: " & strManu & vbNewLine & _
			 "Model: " & strModel

	Wscript.Echo output
Next
