var objWMIService = GetObject("winmgmts:\\\\.\\root\\cimv2");
var objList = objWMIService.ExecQuery("SELECT * FROM Win32_ComputerSystem");
var objItem = new Enumerator(objList);
for (; !objItem.atEnd(); objItem.moveNext()) {
  var strDomain = objItem.item().Domain;
  var strName = objItem.item().Name;
  var strManu = objItem.item().Manufacturer;
  var strModel = objItem.item().Model;

  var output = "Domain: " + strDomain + "\n" +
               "Computer Name: " + strName + "\n" +
               "Manufacturer: " + strManu + "\n" +
               "Model: " + strModel;

  WScript.Echo(output);
}
