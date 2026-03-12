/**
 * Cookiebro
 *
 * Advanced cookie manager WebExtension by Nodetics <nodetics@gmail.com>
 * All Rights Reserved (C)
 */
var _whitelist;
var _blacklist;
var _whitelistedCookies;
var _blacklistedCookies;
var _cookieStoreId;

$(document).ready(function() {
	
	var param = getQueryParams(document.location.search);
	_cookieStoreId = param.store;
	
	chrome.runtime.sendMessage({command: "getoptions"}, function(response) {
		
		_whitelist = response.whitelist;
		_blacklist = response.blacklist;
		_whitelistedCookies = response.whitelistedCookies;
		_blacklistedCookies = response.blacklistedCookies;
		
		drawList(_whitelist, "white");
		drawList(_blacklist, "black");
		
		var settings = response.settings;
		
		$("button.clearcookies").click(function() {
			var elem = $(this);
			var type = elem.attr("data-type"); // unwanted, session-all, session-nonwhitelisted
			if( type == "unwanted" )
			{
				chrome.runtime.sendMessage({command: "purge", storeId: _cookieStoreId}, function(response) {
					drawCookielist();
				});
			}
			if( type == "session-all" )
			{
				chrome.runtime.sendMessage({command: "purgesession", storeId: _cookieStoreId}, function(response) {
					drawCookielist();
				});
			}
			if( type == "session-nonwhitelisted" )
			{
				chrome.runtime.sendMessage({command: "purgesession-nonwhitelisted", storeId: _cookieStoreId}, function(response) {
					drawCookielist();
				});
			}
		});
		
		$("input#startupdelete").prop("checked", settings.startupdelete);
		$("input#startupdelete").change(function() {
			var box = $(this);
			updateSetting("startupdelete", box.prop("checked"));
		});

		$("input#startuppluginpurge").prop("checked", settings.startuppluginpurge);
		$("input#startuppluginpurge").change(function() {
			var box = $(this);
			updateSetting("startuppluginpurge", box.prop("checked"));
		});
		
		$("input#dynamicicon").prop("checked", settings.dynamicicon);
		$("input#dynamicicon").change(function() {
			var box = $(this);
			updateSetting("dynamicicon", box.prop("checked"));
		});
		
		$("input#startupbrowsingpurge").prop("checked", settings.startupbrowsingpurge);
		$("input#startupbrowsingpurge").change(function() {
			var box = $(this);
			updateSetting("startupbrowsingpurge", box.prop("checked"));
		});

		$("input#startupserviceworkerpurge").prop("checked", settings.startupserviceworkerpurge);
		$("input#startupserviceworkerpurge").change(function() {
			var box = $(this);
			updateSetting("startupserviceworkerpurge", box.prop("checked"));
		});

		$("input#keepsession").prop("checked", settings.keepsession);
		$("input#keepsession").change(function() {
			var box = $(this);
			updateSetting("keepsession", box.prop("checked"));
		});

		$("input#blacklistsession").prop("checked", settings.blacklistsession);
		$("input#blacklistsession").change(function() {
			var box = $(this);
			updateSetting("blacklistsession", box.prop("checked"));
		});
		
		$("input#blacklist").prop("checked", settings.blacklist);
		$("input#blacklist").change(function() {
			var box = $(this);
			updateSetting("blacklist", box.prop("checked"));
		});

		$("input#disablefavicons").prop("checked", settings.disablefavicons);
		$("input#disablefavicons").change(function() {
			var box = $(this);
			updateSetting("disablefavicons", box.prop("checked"));
		});

		$("input#disablecookielog").prop("checked", settings.disablecookielog);
		$("input#disablecookielog").change(function() {
			var box = $(this);
			updateSetting("disablecookielog", box.prop("checked"));
		});
		
		$("input#filterLink").prop("checked", settings.filterLink);
		$("input#filterLink").change(function() {
			var box = $(this);
			updateSetting("filterLink", box.prop("checked"));
		});

		$("input#filterEtag").prop("checked", settings.filterEtag);
		$("input#filterEtag").change(function() {
			var box = $(this);
			updateSetting("filterEtag", box.prop("checked"));
		});
		
		$("select#period").val(settings.period);
		$("select#period").change(function() {
			var select = $(this);
			updateSetting("period", parseInt(select.val(), 10));
		});

		$("input#newdomainwhite").keydown(function(event) {
			if (event.keyCode == 13) {
				$("button#addnewwhite").click();
			}
		});
		
		$("button#addnewwhite").click(function() {
			var input = $("input#newdomainwhite");
			var domain = input.val();
			if( domain && domain.length > 1 && domain.charAt(0) == '*' )
			{
				domain = domain.substring(1); // strip away the first *
			}
			if( domain.indexOf("://") != -1 )
			{
				alert("Please enter a domain name like www.google.com or domain wilcard like *.google.com - not an URL");
				return;
			}
			
			input.val("");
			input.focus();
			
			var i = domain.indexOf("/");
			
			if( i != -1 )
			{
				// set named cookie
				var cookie = {domain: domain.substring(0, i), name: domain.substring(i + 1).trim()};
				chrome.runtime.sendMessage({command: "setwhitelisted", cookie: cookie, bool: true}, function(response) {
					if( _whitelistedCookies[cookie.domain] == undefined )
					{
						_whitelistedCookies[cookie.domain] = {};
					}
					_whitelistedCookies[cookie.domain][cookie.name] = true;
					drawList(_whitelist, "white");
				});
			}
			else
			{
				if( _whitelist[domain] )
				{
					return; // already present
				}
				chrome.runtime.sendMessage({command: "whitelist", host: domain}, function(response) {
					_whitelist[domain] = true;
					drawList(_whitelist, "white");
				});
			}
		});

		$("input#newdomainblack").keydown(function(event) {
			if (event.keyCode == 13) {
				$("button#addnewblack").click();
			}
		});
		
		$("button#addnewblack").click(function() {
			var input = $("input#newdomainblack");
			var domain = input.val();
			if( domain && domain.length > 1 && domain.charAt(0) == '*' )
			{
				domain = domain.substring(1); // strip away the first *
			}
			if( domain.indexOf("://") != -1 )
			{
				alert("Please enter a domain name like www.google.com or domain wilcard like *.google.com - not an URL");
				return;
			}
			input.val("");
			input.focus();
			
			var i = domain.indexOf("/");
			
			if( i != -1 )
			{
				// set named cookie
				var cookie = {domain: domain.substring(0, i), name: domain.substring(i + 1).trim()};
				chrome.runtime.sendMessage({command: "setblacklisted", cookie: cookie, bool: true}, function(response) {
					if( _blacklistedCookies[cookie.domain] == undefined )
					{
						_blacklistedCookies[cookie.domain] = {};
					}
					_blacklistedCookies[cookie.domain][cookie.name] = true;
					drawList(_blacklist, "black");
				});
			}
			else
			{
				if( _blacklist[domain] )
				{
					return; // already present
				}
				chrome.runtime.sendMessage({command: "blacklist", host: domain}, function(response) {
					_blacklist[domain] = true;
					drawList(_blacklist, "black");
				});
			}
		});
		
		$("button#exportwhite").click(function() {
			exportList(_whitelist, "white");
		});
		
		$("button#importwhite").click(function() {
			$("input#whitefileupload").click(); 
			return false; 
		});			
		
		$("input#whitefileupload").change(function() { 
			readFile("input#whitefileupload", importList, "white");
			return false; 
		});

		$("button#importblack").click(function() {
			$("input#blackfileupload").click(); 
			return false; 
		});			
		
		$("input#blackfileupload").change(function() { 
			readFile("input#blackfileupload", importList, "black");
			return false; 
		});
		
		$("button#exportblack").click(function() {
			exportList(_blacklist, "black");
		});
		
		$("button#clearwhite").click(function() {
			chrome.runtime.sendMessage({command: "clearwhitelist"}, function(response) {
				_whitelist = {};
				_whitelistedCookies = {};
				drawList(_whitelist, "white");
			});
		});

		$("button#clearblack").click(function() {
			chrome.runtime.sendMessage({command: "clearblacklist"}, function(response) {
				_blacklist = {};
				_blacklistedCookies = {};
				drawList(_blacklist, "black");
			});
		});

		$("button#purgebrowsingdata").click(function() {
			chrome.runtime.sendMessage({command: "purgebrowsingdata"}, function(response) {
				alert("Stored Website Data Cleared");
			});
		});
		
		$("button#deleteall").click(function() {
			if( confirm("Are you absolutely certain that you want to delete ALL cookies (including whitelisted cookies)?") )
			{
				chrome.runtime.sendMessage({command: "deleteall"}, function(response) {
					alert("All cookies deleted!");
					document.location.reload();
				});
			}
		});
		
		$("#viewhelp").click(viewHelp);
		
		drawCookielist();
	});
});

function exportList(list, type)
{
	var i, j, result = "", hosts = Object.keys(list), names, host;
	hosts = sortHosts(hosts);
	for(i = 0; i < hosts.length; i++)
	{
		if( hosts[i].charAt(0) == '.' )
		{
			result += "*";
		}
		result += hosts[i];
		if( i + 1 < hosts.length )
		{
			result += "\n";
		}
	}
	var cookieMap;
	if( type == "white" )
	{
		cookieMap = _whitelistedCookies;
	}
	else if( type == "black" )
	{
		cookieMap = _blacklistedCookies;
	}
	else
	{
		throw new Error("Undefined list type: " + type);
	}
	hosts = Object.keys(cookieMap);
	var extraResult = "";
	
	for(i = 0; i < hosts.length; i++)
	{
		host = hosts[i];
		names = Object.keys(cookieMap[host]);
		for(j = 0; j < names.length; j++)
		{
			if( host.length > 0 && host.charAt(0) == '.' )
			{
				extraResult += "*";
			}
			extraResult += host + "/" + names[j];
			if( j + 1 < names.length )
			{
				extraResult += "\n";
			}
		}
	}
	if( extraResult != "" )
	{
		result += "\n# -------------------------------------------------------------------------- \n";
		result += "# Single cookie settings:\n";
		result += "# -------------------------------------------------------------------------- \n";
		result += extraResult;
	}
	
	downloadFile(result, "cookiebro-" + type + "list.txt", "text/plain");
}

function importList(contents, file, type)
{
	var lines = contents.split("\n");
	var line, i, j, is = lines.length, host, name;
	var result = [];
	var cookieMap = {};
	for(i = 0; i < is; i++)
	{
		line = lines[i];
		line = line.trim(); // remove whitespace, \r, tab etc
		if( line && line.length > 0 && line.charAt(0) == '#' )
		{
			continue; // skip comment lines starting with #
		}
		if( line && line.length > 2 && line.charAt(0) == '/' && line.charAt(1) == '/' )
		{
			continue; // skip comment lines starting with //
		}
		if( line.indexOf('.') == -1 )
		{
			continue; // skip lines that clearly aren't domain names
		}
		if( line.charAt(0) == '*' )
		{
			line = line.substring(1); // strip away the * since internal representation is: .google.com (not *.google.com)
		}
		// *.google.com/NCID  refers to a cookie with name NCID
		j = line.indexOf('/');
		if( j != -1 )
		{
			host = line.substring(0, j);
			name = line.substring(j + 1).trim();
			if( cookieMap[host] == undefined )
			{
				cookieMap[host] = {};
			}
			cookieMap[host][name] = true;
		}
		else
		{
			result.push(line);
		}
	}
	chrome.runtime.sendMessage({command: "import" + type + "list", lines: result, cookieMap: cookieMap}, function(response) {
		document.location.reload();
	});
}

function drawCookielist(storeId)
{
	if( storeId == undefined )
	{
		storeId = _cookieStoreId;
	}
	chrome.runtime.sendMessage({command: "getcookies", storeId: storeId}, function(response) {
		var sorted = response.cookies;
		drawHostlist(sorted.whitelisted, "div#whitelistedCookies");
		drawHostlist(sorted.unwanted, "div#unwantedCookies");
		drawHostlist(sorted.session, "div#sessionCookies");
	});
}

function drawHostlist(map, containerId)
{
	var i, hosts, html;
	
	hosts = Object.keys(map);
	hosts = sortHosts(hosts);
	if( hosts.length > 0 )
	{
		html = "<table>";
		for(i = 0; i < hosts.length; i++)
		{
			html += "<tr><td class='hostcolumn'><span class='hostname'>";
			if( hosts[i] == "" ) {
				html += "(empty domain)";
			}
			else {
				html += escapeHtml(hosts[i]);
			}
			html += "</span></td><td><span class='cookiecount'>(" + map[hosts[i]] + ")</span></td>";
			if( containerId == "div#unwantedCookies" )
			{
				html += "<td data-host='" + escapeHtml(hosts[i]) + "'><a href='#' class='hostlink' title='Add to whitelist' data-op='white'>+Whitelist</a> <a href='#' class='hostlink' title='Add to blacklist' data-op='black'>+Blacklist</a></td>";
			}
			else
			{
				html += "<td></td>";
			}
			html += "</tr>";
		}
		html += "</table>";
	}
	else
	{
		html = "<br><div>None</div>";
	}
	$(containerId).html(html);
	$("a.hostlink").click(function() {
		var elem = $(this);
		var host = elem.parent().attr("data-host");
		var op = elem.attr("data-op");
		
		var map;
		if( op == "white" )
		{
			map = _whitelist;
		}
		if( op == "black" )
		{
			map = _blacklist;
		}
		
		if( map[host] )
		{
			return; // already present
		}
		
		flashElement(elem);
		
		chrome.runtime.sendMessage({command: op + "list", host: host}, function(response) {
			map[host] = true;
			drawList(map, op);
		});
		return false;
	});
}

function drawList(list, type)
{
	var i, hosts = Object.keys(list);
	
	hosts = sortHosts(hosts);
	
	var html = "<table>";
	for(i = 0; i < hosts.length; i++)
	{
		var subs = false;
		if( hosts[i].charAt(0) == '.' )
		{
			subs = true;
		}
		
		html += "<tr>";
		html += "<td class='hostcolumn'><span class='hostname'>" +  escapeHtml((subs ? "*" : "") + hosts[i]) + "</span></td>";
		html += "<td><span class='hostaction' data-action='remove' data-host='" +  escapeHtml(hosts[i]) + "'>Remove</span></td>";
		html += "</tr>";
	}
	
	// list individual cookie settings
	var host, names, j;
	var cookieMap;
	if( type == "white" )
	{
		cookieMap = _whitelistedCookies;
	}
	else if( type == "black" )
	{
		cookieMap = _blacklistedCookies;
	}
	hosts = Object.keys(cookieMap);
	for(i = 0; i < hosts.length; i++)
	{
		host = hosts[i];
		names = Object.keys(cookieMap[host]);
		for(j = 0; j < names.length; j++)
		{
			html += "<tr>";
			html += "<td class='hostcolumn'><span class='" + type + "cookiename'>" + escapeHtml((host.charAt(0) == '.' ? "*" : "") + host + "/" + names[j]) + "</span></td>";
			html += "<td><span class='hostaction' data-action='removecookiesetting' data-host='" + escapeHtml(host) + "' data-name='" + escapeHtml(names[j]) + "'>Remove</span></td>";
			html += "</tr>";
		}
	}
	
	html += "</table>";
	
	$("div#" + type + "list").empty().html(html);
	
	$("div#" + type + "list span.hostaction").click(function() {
		var elem = $(this);
		var action = elem.attr("data-action"); // remove, edit
		var host = elem.attr("data-host");
		var name;
		
		if( action == "remove" )
		{
			chrome.runtime.sendMessage({command: "remove" + type, host: host}, function(response) {
				delete list[host];
				// drawList(list, type);
				elem.parent().parent().remove();
			});
		}
		else if( action == "removecookiesetting" )
		{
			name = elem.attr("data-name");
			chrome.runtime.sendMessage({command: "set" + type + "listed", cookie: {domain: host, name: name}, bool: false}, function(response) {
				if( type == "white" && _whitelistedCookies[host] )
				{
					delete _whitelistedCookies[host][name];
				}
				if( type == "black" && _blacklistedCookies[host] )
				{
					delete _blacklistedCookies[host][name];
				}
				// drawList(list, type);
				elem.parent().parent().remove();
			});
		}
	});
}

function updateSetting(key, value, callback)
{
	chrome.runtime.sendMessage({command: "updatesetting", key: key, value: value}, function(response) {
		console.log("Updated " + key + " = " + value);
		if( callback )
		{
			callback();
		}
	});
}

function flashElement(elem)
{
	elem.fadeTo(300, 0.2, function() { $(this).fadeTo(800, 1.0); });
}

function viewHelp()
{
	var width = 1024;
	var height = 850;
	
	if( height > screen.height ) {
		height = screen.height - 50;
	}
	
	var left = Math.round( (screen.width / 2) - (width / 2) );
	var top = Math.round( (screen.height / 2) - (height / 2) );

	chrome.windows.create({'url': chrome.runtime.getURL("help.html"), 'type': 'popup', 'width': width, 'height': height, 'top': top, 'left': left});
}
