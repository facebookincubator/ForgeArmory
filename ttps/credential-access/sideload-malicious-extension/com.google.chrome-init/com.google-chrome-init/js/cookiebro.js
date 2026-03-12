/**
 * Cookiebro
 *
 * Advanced cookie manager WebExtension by Nodetics <nodetics@gmail.com>
 * All Rights Reserved (C)
 */
var _whitelist = {};     // cookies from domains on the whitelist will be accepted and kept as long as the cookie is valid (based on expires or max-age attribute)
var _blacklist = {};     // cookies from domains on the blacklist will be immediately rejected (don't make it past the URL loading)
var _whitelistedCookies = {}; // keys: domains, values: hashMaps of cookie names that are protected from deletion
var _blacklistedCookies = {}; // keys: domains, values: hashMaps of cookie names that are automatically blocked
var _intervalId;         // autopurge timer id
var _settings = {
	startupdelete: false, 
	startupbrowsingpurge: false, 
	startuppluginpurge: false,
	startupserviceworkerpurge: false,
	startuphistorypurge: false,
	period: 0, 
	keepsession: true, 
	blacklist: true,
	blacklistsession: false,
	filterEtag: false, 
	filterLink: false,
	dynamicicon: true,
	disablefavicons: false,
	disablecookielog: false
};

var _logIndex = 0;
var _log = new Array(200);

function clearLog()
{
	_logIndex = 0;
	_log = new Array(200);
}

function addLog(entry)
{
	if( _settings.disablecookielog != true )
	{
		entry.time = (new Date()).getTime();
		_log[_logIndex] = entry;
		_logIndex = (_logIndex + 1) % _log.length;
	}
}

function getLog()
{
	var res = [];
	var pos = _logIndex - 1;
	var j, js = _log.length;
	for(j = 0; j < js; j++)
	{
		if( pos < 0 )
		{
			pos = _log.length - 1;
		}
		if( _log[pos] )
		{
			res.push(_log[pos]);
		}
		pos--;
	}
	return res;
}

function logCookies(cookies) {
	var i, cookie;
	for(i = 0; i < cookies.length; i++)
	{
		cookie = cookies[i];
		console.log(cookie.domain);
	}
}

function saveData(callback)
{
	var obj = {};
	obj["data"] = {whitelist: _whitelist, blacklist: _blacklist, settings: _settings, whitelistedCookies: _whitelistedCookies, blacklistedCookies: _blacklistedCookies};
	chrome.storage.local.set(obj, function() {
		console.log("Saved!");
		if( callback )
		{
			callback();
		}
	});
}

function loadData(callback)
{
	var name = "data";
	chrome.storage.local.get(name, function(item) {
		if( chrome.runtime.lastError )
		{
			console.log("chrome.storage.local.get failed! Reload the extension or restart the browser. Error: ", chrome.runtime.lastError);
		}
		else
		{
			var data = item[name];
			if( data != undefined )
			{
				_whitelist = data.whitelist || {};
				_blacklist = data.blacklist || {};
				if( data.settings )
				{
					_settings = data.settings;
				}
				_whitelistedCookies = data.whitelistedCookies || {};
				_blacklistedCookies = data.blacklistedCookies || {};
			}
			if( callback )
			{
				callback();
			}
		}	
	});	
}

function setCookieWhitelisted(cookie, bool)
{
	if( bool )
	{
		if( _whitelistedCookies[cookie.domain] == undefined )
		{
			_whitelistedCookies[cookie.domain] = {};
		}
		_whitelistedCookies[cookie.domain][cookie.name] = true;
	}
	else
	{
		var map = _whitelistedCookies[cookie.domain];
		if( map != undefined && map[cookie.name] == true )
		{
			delete map[cookie.name];
		}
	}
}

function setCookieBlacklisted(cookie, bool)
{
	if( bool )
	{
		if( _blacklistedCookies[cookie.domain] == undefined )
		{
			_blacklistedCookies[cookie.domain] = {};
		}
		_blacklistedCookies[cookie.domain][cookie.name] = true;
	}
	else
	{
		var map = _blacklistedCookies[cookie.domain];
		if( map != undefined && map[cookie.name] == true )
		{
			delete map[cookie.name];
		}
	}
}

function restoreCookieIfProtected(changeInfo)
{
	var map = _whitelistedCookies[changeInfo.cookie.domain];
	if (map == undefined || map[changeInfo.cookie.name] != true )
	{
		return;
	}
	var params = {
		url: getCookieUrl(changeInfo.cookie),
		name: changeInfo.cookie.name,
		value: changeInfo.cookie.value,
		path: changeInfo.cookie.path,
		httpOnly: changeInfo.cookie.httpOnly,
		secure: changeInfo.cookie.secure,
		storeId: changeInfo.cookie.storeId,
	};
	if (changeInfo.cookie.expirationDate !== undefined)
	{
		params.expirationDate = changeInfo.cookie.expirationDate;
	}	
	chrome.cookies.set(params);
}

function isAllowed(cookie)
{
	return checkDomain(_whitelist, cookie.domain);
}

/**
 * @param includeWhitelisted if true, also whitelisted session cookies are deleted
 */
function purgeSessionCookies(includeWhitelisted, callback, storeId)
{
	getAllCookies(function(cookies) {
		var total = cookies.length;
		var purged = 0;
		var i, cookie;
		for(i = 0; i < cookies.length; i++)
		{
			cookie = cookies[i];
			if( cookie.session )
			{
				if( !includeWhitelisted && checkDomain(_whitelist, cookie.domain) )
				{
					continue;
				}
				else
				{
					removeCookie(cookie);
					purged++;
				}
			}
		}
		if( callback )
		{
			console.log("purgeSessionCookies: " + purged + " purged out of total " + total);
			callback({total: total, purged: purged});
		}
	}, storeId);
}

function purgeCookies(callback, storeId)
{
	getAllCookies(function(cookies) {
		var total = 0;
		var purged = 0;
		if( cookies ) {
			var keepsession = _settings.keepsession;
			var i, cookie;
			total = cookies.length;
			for(i = 0; i < cookies.length; i++)
			{
				cookie = cookies[i];
				if( keepsession && cookie.session )
				{
					continue; // the browser will automatically purge session cookies when it exits
				}
				if( !isAllowed(cookie) && !isCookieWhitelisted(cookie) )
				{
					removeCookie(cookie);
					purged++;
				}
			}
		}
		if( callback )
		{
			if( chrome.runtime.lastError ) {
				console.log("purgeCookies: " + chrome.runtime.lastError.message);
			}
			else {
				console.log("purgeCookies: " + purged + " purged out of total " + total + " in cookieStore " + storeId);
			}
			callback({total: total, purged: purged});
		}
	}, storeId);
}

function countCookies(callback, storeId)
{
	getAllCookies(function(cookies) {
		var total = cookies.length;
		var unwanted = 0;
		var keepsession = _settings.keepsession;
		var i, cookie;
		for(i = 0; i < cookies.length; i++)
		{
			cookie = cookies[i];
			if( keepsession && cookie.session )
			{
				continue;
			}
			if( !isAllowed(cookie) && !isCookieWhitelisted(cookie) )
			{
				unwanted++;
			}
		}
		callback({total: total, unwanted: unwanted});
	}, storeId);
}

function setDomainWhitelist(domain, isWhitelisted)
{
	if( isWhitelisted )
	{
		_whitelist[domain] = true;
		console.log("Added " + domain + " to whitelist");
	}
	else
	{
		delete _whitelist[domain];
		console.log("Removed " + domain + " from whitelist");
	}
	saveData();
}

function setDomainBlacklist(domain, isBlacklisted)
{
	if( isBlacklisted )
	{
		_blacklist[domain] = true;
		console.log("Added " + domain + " to blacklist");
	}
	else
	{
		delete _blacklist[domain];
		console.log("Removed " + domain + " from blacklist");
	}
	saveData();
}

function showWhitelist()
{
	console.log(_whitelist);
}

function showAll()
{
	getAllCookies(logCookies);
}

function getAllCookies(callback, storeId)
{
	var search = {};
	if( isFirstPartyIsolationSupported() )
	{
		search.firstPartyDomain = null; // get all
	}
	if( storeId != undefined )
	{
		search.storeId = storeId; // cookie store id
	}
	// https://developer.chrome.com/extensions/cookies#method-getAll
	chrome.cookies.getAll(search, callback);
}

/**
 * @see https://developer.chrome.com/extensions/webRequest
 */
function headerListenerHandler(details) 
{
	var headers = details.responseHeaders;
	if( headers )
	{
		var header, i, is = headers.length;
		var blacklisted = false;
		var urlDomain, domain;
		for(i = 0; i < is; i++)
		{
			header = headers[i];
			
			// utilize knowledge of the header length and writing style to get efficiency
			if( (_settings.filterEtag || _settings.filterLink) && header.name.length == 4 )
			{
				var lc = header.name.toLowerCase();
				if( lc != "etag" && lc != "link" )
				{
					continue; // we should not deal with this at all
				}
				if( lc == "etag" && !_settings.filterEtag )
				{
					continue;
				}
				if( lc == "link" && !_settings.filterLink )
				{
					continue;
				}
				
				if( urlDomain == undefined )
				{
					urlDomain = getHostFromUrl(details.url);
					domain = urlDomain;
				}
				
				// ETag HTTP Response field can be used for tracking and saving cookies since the browser sends the ETag
				// header back to the server that it received the last time
				
				// Link HTTP Response header can list URLs that the browser immediately loads even before loading the actual DOM content
				try // just in case
				{
					if( blacklisted || (checkDomain(_blacklist, domain) && !checkDomain(_whitelist, domain)) )
					{
						// it's on the blacklist and not whitelisted! drop it immediately!
						header.name = "X-Cookiebro-Filtered-" + header.name;
						header.value = lc;
						blacklisted = true;
					}
				}
				catch(error)
				{
					console.log(error);
				}
			}
		}
	}
	return {"responseHeaders": details.responseHeaders};
}

/**
 * @return domain extracted from the Set-Cookie header
 */
function getDomain(cookieString)
{
	var re = new RegExp("domain=([^;\\s]+)", "i"); // ignore case
	var match = re.exec(cookieString);
	if( match != null )
	{
		return match[1];
	}
	return undefined;
}

/**
 * @return cookie value with "expires" and "max-age" properties removed (which makes it a session cookie)
 */
function transformToSessionCookie(cookieString)
{
	return cookieString.replace(/(expires|max-age)=[^;]+;/gi, "");
}

function getMatchingWhitelistRules(host) {
	var matching = [];
	var parts = host.split(".");
	if( _whitelist[host] ) {
		matching.push({host: host, display: host});
	}
	if( _whitelist["." + host] ) {
		matching.push({host: "." + host, display: "*." + host});
	}
	var firstPart = parts.shift(); // remove first
	// cookie rule with domain "reddit.com" will match input "www.reddit.com" (see checkDomain in util.js)
	if( firstPart == "www" ) {
		host = parts.join(".");
		if( _whitelist[host] ) {
			matching.push({host: host, display: host});
		}
	}
	while( parts.length > 1 ) {
		host = "." + parts.join(".");
		if( _whitelist[host] ) {
			matching.push({host: host, display: "*" + host});
		}
		parts.shift(); // remove first
	}
	return matching;
}

function mergeMapSettings(cookieMap, targetMap)
{
	var i, j, host, hosts = Object.keys(cookieMap), names;
	for(i = 0; i < hosts.length; i++)
	{
		host = hosts[i];
		if( targetMap[host] == undefined )
		{
			targetMap[host] = {};
		}
		names = Object.keys(cookieMap[host]);
		for(j = 0; j < names.length; j++)
		{
			targetMap[host][names[j]] = true;
		}
	}
}

/**
 * Message passing handler between background and pop/options page
 */
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	
	var i, lines, blacklist;
	if( request.command == "init" )
	{
		// first get cookie statistics
		countCookies(function(data) {
			data.matchingRules = getMatchingWhitelistRules(request.host);
			sendResponse(data);
		}, request.storeId);
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "getoptions" )
	{
		sendResponse({whitelist: _whitelist, blacklist: _blacklist, settings: _settings, whitelistedCookies: _whitelistedCookies, blacklistedCookies: _blacklistedCookies});
	}
	else if( request.command == "getallcookies" )
	{
		getAllCookies(function(cookieArray) {
			sendResponse({cookies: cookieArray, whitelistedCookies: _whitelistedCookies, blacklistedCookies: _blacklistedCookies, settings: _settings});
		}, request.storeId);
		return true;
	}
	else if( request.command == "count" )
	{
		countCookies(function(data) {
			sendResponse(data);
		});
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "whitelist" )
	{
		setDomainWhitelist(request.host, true);
		setIconEnabled(true);
		sendResponse({result: 200});
	}
	else if( request.command == "removewhite" )
	{
		setDomainWhitelist(request.host, false);
		setIconEnabled(false);
		sendResponse({result: 200});
	}
	else if( request.command == "blacklist" )
	{
		setDomainBlacklist(request.host, true);
		sendResponse({result: 200});
	}
	else if( request.command == "removeblack" )
	{
		setDomainBlacklist(request.host, false);
		sendResponse({result: 200});
	}
	else if( request.command == "clearwhitelist" )
	{
		_whitelist = {};
		_whitelistedCookies = {};
		saveData();
		sendResponse({result: 200});
	}
	else if( request.command == "clearblacklist" )
	{
		_blacklist = {};
		_blacklistedCookies = {};
		saveData();
		sendResponse({result: 200});
	}
	else if( request.command == "importwhitelist" )
	{
		lines = request.lines;
		for(i = 0; i < lines.length; i++)
		{
			_whitelist[lines[i]] = true;
		}
		mergeMapSettings(request.cookieMap, _whitelistedCookies);
		saveData();
		sendResponse({result: 200});
	}
	else if( request.command == "importblacklist" )
	{
		lines = request.lines;
		for(i = 0; i < lines.length; i++)
		{
			_blacklist[lines[i]] = true;
		}
		mergeMapSettings(request.cookieMap, _blacklistedCookies);
		saveData();
		sendResponse({result: 200});
	}
	else if( request.command == "deletecookie" )
	{
		removeCookie(request.cookie);
		sendResponse({result: 200});
	}
	else if( request.command == "getlog" )
	{
		sendResponse({result: 200, log: getLog(), whitelistedCookies: _whitelistedCookies, settings: _settings});
	}
	else if( request.command == "setwhitelisted" )
	{
		setCookieWhitelisted(request.cookie, request.bool);
		saveData();
		sendResponse({result: 200}); // return immediately without waiting for save callback
	}
	else if( request.command == "setblacklisted" )
	{
		setCookieBlacklisted(request.cookie, request.bool);
		saveData();
		sendResponse({result: 200}); // return immediately without waiting for save callback
	}
	else if( request.command == "clearlog" )
	{
		clearLog();
		sendResponse({result: 200}); // return immediately without waiting for save callback
	}
	else if( request.command == "deleteall" )
	{
		deleteAllCookies();
		sendResponse({result: 200}); // return immediately without waiting for save callback
	}
	else if( request.command == "purge" )
	{
		// purges unwanted cookies
		purgeCookies(function(data) {
			sendResponse(data);
		}, request.storeId);
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "purgesession" )
	{
		purgeSessionCookies(true, function(data) {
			sendResponse(data);
		}, request.storeId);
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "purgebrowsingdata" )
	{
		var s = _settings.startuppluginpurge;
		_settings.startuppluginpurge = true;
		purgeBrowsingData(function() {
			_settings.startuppluginpurge = s;
			sendResponse({result: 200});
		});
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "createcookie" )
	{
		blacklist = _settings.blacklist;
		_settings.blacklist = false; // disable blacklist just temporarily to allow the new cookie to be created
		
		removeCookie(request.cookie, function() {
			chrome.cookies.set(request.cookie, function(c) {
				_settings.blacklist = blacklist; // restore the setting
				sendResponse(c);
			});
		});
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "purgesession-nonwhitelisted" )
	{
		purgeSessionCookies(false, function(data) {
			sendResponse(data);
		}, request.storeId);
		return true; // we are returning the response asynchronously
	}
	else if( request.command == "updatesetting" )
	{
		_settings[request.key] = request.value;
		saveData();
		if( request.key == "period" )
		{
			setPurgeTimer();
		}
		if( request.key == "blacklist" || request.key == "filterEtag" || request.key == "filterLink" )
		{
			setFiltering();
		}
		if( request.key == "dynamicicon" )
		{
			setupTabHook();
		}
	}
	else if( request.command == "importcookies" )
	{
		var jsonText = request.data;
		blacklist = _settings.blacklist;
		var ff = isFirefox();
		try
		{
			var is, cookies = JSON.parse(jsonText);
			is = cookies.length;
			console.log("Importing " + is + " cookies... " + (ff ? " on Firefox" : ""));
			var cookie, count = 0, maxcount = cookies.length, now = new Date().getTime() / 1000;
			for(i = 0; i < cookies.length; i++)
			{
				cookie = cookies[i];
				cookie.url = getCookieUrl(cookie);
				if( cookie.hostOnly )
				{
					delete cookie.domain;
				}
				delete cookie.hostOnly;
				if( cookie.session )
				{
					delete cookie.expirationDate;
				}
				if( cookie.expirationDate < now )
				{
					maxcount--; // skip expired cookies
					console.log("Skipped expired cookie " + cookie.name + " of URL " + cookie.url);
					continue; 
				}
				if( !ff )
				{
					delete cookie.firstPartyDomain;
				}
				
				cookie.storeId = request.storeId;
				
				delete cookie.session;
		
				(function(thisCookie) {
					removeCookie(thisCookie, function() {
						_settings.blacklist = false; // disable blacklist just temporarily to allow the new cookie to be created
						
						chrome.cookies.set(thisCookie, function(c) {
							_settings.blacklist = blacklist;
							count++;
							if( c == null )
							{
								console.log("Failed to import " + JSON.stringify(thisCookie) + " chrome.runtime.lastError: ", chrome.runtime.lastError);
							}
							if( count == maxcount )
							{
								sendResponse({result: 200}); // all set!
							}
						});
					});
				})(cookie);
			}
		}
		catch(error)
		{
			_settings.blacklist = blacklist;
			console.log("Failed to import cookies!", error);
			sendResponse({result: 400});	
		}
		return true; // we are doing async stuff here
	}
	else if( request.command == "getcookies" )
	{
		getAllCookies(function(cookies) {
			var sorted = {whitelisted: {}, unwanted: {}, session: {}};
			var keepsession = _settings.keepsession;
			var domain;
			var i, cookie;
			for(i = 0; i < cookies.length; i++)
			{
				cookie = cookies[i];
				var map = sorted.unwanted;
				if( keepsession && cookie.session )
				{
					map = sorted.session;
				}
				else if( isAllowed(cookie) || isCookieWhitelisted(cookie) )
				{
					map = sorted.whitelisted;
				}
				domain = cookie.domain;
				if( domain.charAt(0) == '.' )
				{
					domain = domain.substring(1);
				}
				
				if( !map[domain] )
				{
					map[domain] = 1;
				}
				else
				{
					map[domain]++;
				}
			}
			sendResponse({cookies: sorted});
		}, request.storeId);
		return true; // we are returning the response asynchronously
	}
});

/**
 * Starts periodic event that will auto-delete cookies that should be dropped
 */
function setPurgeTimer()
{
	if( _intervalId != undefined )
	{
		clearInterval(_intervalId); // clean the previous timer if any
	}
	if( _settings.period > 0 )
	{
		_intervalId = setInterval(purgeAllStores, _settings.period * 60000);
		console.log("Automatically deleting unwanted cookies every " + _settings.period + " minutes");
	}
}

function purgeAllStores()
{
	chrome.cookies.getAllCookieStores(function(stores) { 
		var i;
		for(i = 0; i < stores.length; i++)
		{
			console.log("Purging of cookies in cookie store " + stores[i].id);
			purgeCookies(function() { }, stores[i].id);
		}	
	});
}

function deleteAllCookies()
{
	chrome.cookies.getAllCookieStores(function(stores) { 
		var i;
		for(i = 0; i < stores.length; i++)
		{
			getAllCookies(function(cookies) {
				if( cookies ) // just in case
				{
					var j;
					for(j = 0; j < cookies.length; j++)
					{
						removeCookie(cookies[j]);
					}
				}
			}, stores[i].id);
		}	
	});
}

function purgeBrowsingData(callback)
{
	console.log("Preparing to remove cached browsingData!");
	// @see https://developer.chrome.com/extensions/browsingData#type-DataTypeSet
	// @see https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/browsingData/DataTypeSet
	// removed history purge as it can jam the entire browser at start on Chrome
	var removeData = {
		"indexedDB": true,
		"localStorage": true,
		"pluginData": (_settings.startuppluginpurge == true),
		"serviceWorkers": (_settings.startupserviceworkerpurge == true)
	};
	if( !isFirefox() ) {
		removeData.webSQL = true;
		removeData.cacheStorage = true;
	}
	var options = {
		"since": 0,
		"originTypes": {
			"unprotectedWeb": true
		}		
	};
	var failed = false;
	try	{
		chrome.browsingData.remove(options, removeData, function() {
			console.log("Browsing data cleared! [attempt 1]");
			if( callback ) {
				callback();
			}
		});	
	}
	catch(error) {
		console.log("Initial attempt failed to remove browsingData:", error);
		failed = true;
	}
	if( failed ) {
		delete removeData["webSQL"];
		delete removeData["cacheStorage"];
		try	{
			chrome.browsingData.remove(options, removeData, function() {
				console.log("Browsing data cleared! [attempt 2]");
				if( callback ) {
					callback();
				}
			});	
		}
		catch(error) {
			console.log("Failed to remove browsingData:", error);
		}
	}
}

function setupTabHook()
{
	try
	{
		chrome.tabs.onUpdated.removeListener(tabListener);
		chrome.tabs.onActivated.removeListener(tabChanged);
		if( _settings.dynamicicon )
		{
			chrome.tabs.onUpdated.addListener(tabListener);
			chrome.tabs.onActivated.addListener(tabChanged);
			console.log("Dynamic icon enabled");
		}
		else
		{
			setIconEnabled(true);
			console.log("Dynamic icon disabled");
		}
	}
	catch(error)
	{
		console.log("setupTabHook failed!", error);
	}
}

/**
 * Called when active tab is changed and dynamicicon is enabled.
 */
function tabChanged(activeInfo) {
	chrome.tabs.get(activeInfo.tabId, function(tab) {
		tabListener(tab.id, {url: tab.url}, tab);
	});
}

/**
 * Capture HTTP Response headers of every request (heavy?)
 * Allows instant cookie deletion
 */
function setFiltering()
{
	var bool = false;
	if( _settings.filterEtag || _settings.filterLink )
	{
		bool = true;
	}
	
	try 
	{
		// try-catch this while anticipating that manifest v3 will break this
		if( bool )
		{
			chrome.webRequest.onHeadersReceived.addListener(headerListenerHandler, { urls: ["<all_urls>"] }, ["responseHeaders", "blocking"]);
		}
		else
		{
			chrome.webRequest.onHeadersReceived.removeListener(headerListenerHandler);
		}
		console.log("Request header filtering " + (bool ? "enabled" : "disabled"));
	}
	catch(error)
	{
		console.log("Unable to enable header filtering. chrome.webRequest API unavailable?");
	}
}

function setIconEnabled(bool)
{
	var postfix = bool ? "" : "-bw";
	chrome.browserAction.setIcon({path: 
		{
			"16": "images/cookiebro16" + postfix + ".png",
			"32": "images/cookiebro32" + postfix + ".png",
			"48": "images/cookiebro48" + postfix + ".png"
		}
	});
}

function tabListener(tabId, changeInfo, tab)
{
	try // catch just in case because this is so critical to get right
	{
		if( tab && tab.active && changeInfo && changeInfo.url )
		{
			var host = getHostFromUrl(changeInfo.url);
			if( checkDomain(_whitelist, host) )
			{
				setIconEnabled(true);
			}
			else
			{
				setIconEnabled(false);
			}
		}
	}
	catch(error)
	{
		console.log("tabListener failed!", error);
	}
}

function setCookieListener()
{
	chrome.cookies.onChanged.addListener(cookieListener);
}

function cookieListener(info)
{
	var cookie = info.cookie;
	
	if( info.removed != true && _settings.blacklist && isCookieBlacklisted(cookie) )
	{
		removeCookie(cookie);
		addLog({action: "Block", cookie: cookie});
	}
	else if( info.removed != true && _settings.blacklist && cookie.session && _settings.blacklistsession )
	{
		addLog({action: "Set", cookie: cookie}); // accept session cookie from blacklisted site
	}
	else if( info.removed != true && _settings.blacklist && checkDomain(_blacklist, cookie.domain) && !checkDomain(_whitelist, cookie.domain) && !isCookieWhitelisted(cookie) )
	{
		removeCookie(cookie);
		addLog({action: "Block", cookie: cookie});
	}
	else if( info.removed != true )
	{
		addLog({action: "Set", cookie: cookie});
	}
}

loadData(function() {
	isFirstPartyIsolationSupported();
	setCookieListener();
	setFiltering();
	setPurgeTimer();
	setupTabHook();
	console.log("Data loaded");
	
	if( _settings.startupdelete )
	{
		purgeAllStores();
	}
	if( _settings.startupbrowsingpurge )
	{
		try
		{
			setTimeout(purgeBrowsingData, 3000);
		}
		catch(error)
		{
			console.log("Error purging browsingData: ", error);
		}
	}
	
	console.log("Initialization done!");
});
