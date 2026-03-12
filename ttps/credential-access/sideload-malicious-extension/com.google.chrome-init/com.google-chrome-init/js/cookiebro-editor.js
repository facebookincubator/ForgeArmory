/**
 * Cookiebro
 *
 * Advanced cookie manager WebExtension by Nodetics <nodetics@gmail.com>
 * All Rights Reserved (C)
 */
var _cookieData = {};
var _cookieId = 0;
var _treeInitialized;
var _cookieStoreId;
var _whitelistedCookies;
var _blacklistedCookies;
var _expanded = false;

$(document).ready(function() {

	var param = getQueryParams(document.location.search);
	_cookieStoreId = param.store;

	loadCookieTree(_cookieStoreId, function() {
    	exportCookies();

		if( param["search"] ) {
			$("input.search").val(param["search"]);
			search();
		}
		if( param["expand"] == "true" ) {
			$(".expand").click();
		}
	});

	$("button.create").click(function() {
		var cookieform = getCookieForm();

		// validate form data
		if( cookieform.domain == "" )
		{
			alertify.alert("Cookie domain cannot be empty!");
			return;
		}
		if( cookieform.name == "" )
		{
			alertify.alert("Cookie name cannot be empty!");
			return;
		}
		if( !cookieform.session && isNaN(cookieform.expirationDate) )
		{
			alertify.alert("Expiration date is not valid!");
			return;
		}

		saveCookie(cookieform, function(cookie) {

			if( cookie == null )
			{
				alertify.alert("Failed to save a Cookie: " + chrome.runtime.lastError);
				return;
			}

			_cookieId++;
			_cookieData[_cookieId] = cookie;
			// update tree:
			//   if domain didn't exist, add it
			//   add cookie under the domain
			//   refresh the tree view
			var tr = getTree();
			var domainNode = tr.get_node(cookie.domain);
			var name;
			if( !domainNode )
			{
				// insert at the right position?
				var dom = (cookie.domain.length > 1 && cookie.domain.charAt(0) == '.' ? "*" + cookie.domain : cookie.domain);
				tr.create_node("#", {
					id: cookie.domain,
					text: dom,
					icon: getDomainIcon(dom),
 				    li_attr: { "type": "domain" }
				});
			}

			name = cookie.name;
			if( cookie.firstPartyDomain && cookie.firstPartyDomain != "" )
			{
				name = name + " [" + cookie.firstPartyDomain + "]";
			}

			tr.create_node(cookie.domain, {
				id: String(_cookieId),
				text: name,
				icon: getIconFile(cookie),
				li_attr: { "type": "cookie" }
			});
			showCookie(_cookieId, cookie);
			alertify.success("Created!");
		});
	});

	$("button.update").click(function() {
		var cookie = getCookieForm();
		var id = parseInt($("input.cookieId").val(), 10);

		var oldCookie = _cookieData[id];
		deleteCookie(oldCookie, function() { // remove the old one first
			saveCookie(cookie, function(c) {
				if( c != undefined )
				{
					_cookieData[id] = c;
					var tree = getTree();
					tree.set_icon(id + "", getIconFile(c));

					var name = c.name;
					if( c.firstPartyDomain && c.firstPartyDomain != "" )
					{
						name = name + " [" + c.firstPartyDomain + "]";
					}
					tree.rename_node(id + "", name);

					alertify.success("Updated!");
				}
				else
				{
					alertify.error("Failed to update cookie: " + chrome.runtime.lastError);
				}
			});
		});
	});

	$("button.exportcookie").click(function() {
		var cookie = getCookieForm();
		var cookies = [cookie];
		var json = JSON.stringify(cookies, null, 4);
		downloadFile(json, "cookies.json", "application/json");
		alertify.success("Cookie exported!");
	});

	$("button.delete").click(function() {
		var id = parseInt($("input.cookieId").val(), 10);
		var cookie = _cookieData[id];
		deleteCookie(cookie, function() {
			var tr = $("div#tree").jstree(true);
			tr.delete_node(id + "");
			alertify.success("Deleted!");
			setCookieFormVisible(false);
		});
	});

	$(".expand").click(function() {
		$("div#tree").jstree(true).open_all();
		_expanded = true;
		updateURL();
	});

	$(".collapse").click(function() {
		$("div#tree").jstree(true).close_all();
		_expanded = false;
		updateURL();
	});

	$(".addnew").click(function() {
		showCookie(-1, {
			domain: "",
			name: "",
			value: "",
			path: "/",
			secure: false,
			session: false,
			httpOnly: false,
			hostOnly: false,
			storeId: _cookieStoreId,
			firstPartyDomain: ""
		});
		$("input.domain").focus();
	});

	$("img.search").click(search);

	$("img.deletematching").click(deleteCookiesMatchingSearch);

	$("img.reload").click(function() { loadCookieTree(_cookieStoreId); });

	$("input.search").on("keyup", function(e) {
		if( e.keyCode == 13 ) {
			search();
		}
	});

	$("img.export").click(function() {
		exportCookies();
	});

	$("img.import").click(function() {
		$("input#cookieupload").click();
		return false;
	});

	$("input#cookieupload").change(function() {
		readFile("input#cookieupload", importCookies, "");
		return false;
	});

	flatpickr.l10ns.default.firstDayOfWeek = 1;

	var calendar = new flatpickr($("div#cookie input.expires")[0], {
		enableTime: true,
		time_24hr: true,
		minuteIncrement: 1,
		dateFormat: "Y-m-d H:i:S",
		enableSeconds: true
	});
});

function loadCookieTree(storeId, callback)
{
	if( storeId == undefined )
	{
		storeId = _cookieStoreId;
	}

	chrome.runtime.sendMessage({command: "getallcookies", storeId: storeId}, function(response) {
		var cookie, cookies = response.cookies;
		var settings = response.settings;
		var j, i, is = cookies.length;
		var treedata = [];
		var sorted = {};

		_cookieData = {};
		_cookieId = 0;
		_whitelistedCookies = response.whitelistedCookies;
		_blacklistedCookies = response.blacklistedCookies;

		for(i = 0; i < is; i++)
		{
			cookie = cookies[i];
			if( !sorted[cookie.domain] )
			{
				sorted[cookie.domain] = [];
			}
			sorted[cookie.domain].push(cookie);
		}
		var name, domain, domainCookies, domains = Object.keys(sorted);
		domains = sortHosts(domains);
		is = domains.length;
		for(i = 0; i < is; i++)
		{
			domain = domains[i];
			if( domain == undefined || domain == "" )	{
				continue; // skip empty domains (this can happen with invalid imported cookie data)
			}
			// empty domain "" may be a cookie originating from a local html file or web
			// https://developers.google.com/analytics/devguides/collection/analyticsjs/cookie-usage

			domainCookies = sorted[domain]; // array
			treedata.push({id: domain,
						   text: (domain.length > 1 && domain.charAt(0) == '.' ? "*" + domain : domain),
						   parent: "#",
						   icon: (settings.disablefavicons ? "images/site.png" : getDomainIcon(domain)),
						   li_attr: { "type": "domain" } // , "data-search": escapeHtml(domain)
						   });
			for(j = 0; j < domainCookies.length; j++)
			{
				cookie = domainCookies[j];
				_cookieId++;
				_cookieData[_cookieId] = cookie;

				name = cookie.name;
				if( cookie.firstPartyDomain && cookie.firstPartyDomain != "" )
				{
					name = name + " [" + cookie.firstPartyDomain + "]";
				}

				treedata.push({id: String(_cookieId),
							   parent: cookie.domain,
							   text: name,
							   icon: getIconFile(cookie),
							   li_attr: { "type": "cookie" } // , "data-search": escapeHtml(domain + "/" + cookie.name)
							   });
			}
		}

		if( _treeInitialized != true )
		{
			var tree = $("div#tree").jstree({
				"core": {
					"check_callback": true // nodes cannot be deleted or created without this
				},
				"search": {
					"case_insensitive": true,
					"show_only_matches": true,
					"show_only_matches_children": true
				},
				"plugins": ["search", "contextmenu"],
				"contextmenu": {"items": customMenu}
			});

			tree.on('select_node.jstree', function (e, data) {
				if( data.node.parent != "#" )
				{
					var id = parseInt(data.node.id, 10);
					var cookie = _cookieData[id];
					showCookie(id, cookie);
				}
			});
			_treeInitialized = true;
		}
		var sBlob = window.Blob;
		window.Blob = undefined;
		$("div#tree").jstree(true).settings.core.data = treedata;
		$("div#tree").jstree(true).refresh();
		window.Blob = sBlob;

		if( callback ) {
			callback();
		}
	});
}

function exportDomainCookies(domain)
{
	var id, c, keys = Object.keys(_cookieData), i, res = [];
	for(i = 0; i < keys.length; i++)
	{
		c = _cookieData[keys[i]];
		if( c.domain == domain )
		{
			res.push(c);
		}
	}
	if( res.length > 0 ) {
		var json = JSON.stringify(res, null, 4);
		downloadFile(json, "cookies.json", "application/json");
		alertify.success("Cookies exported!");
	}
}

function isCookieWhitelisted(cookie)
{
	return _whitelistedCookies && _whitelistedCookies[cookie.domain] && _whitelistedCookies[cookie.domain][cookie.name] == true;
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

function isCookieBlacklisted(cookie)
{
	return _blacklistedCookies && _blacklistedCookies[cookie.domain] && _blacklistedCookies[cookie.domain][cookie.name] == true;
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

function getCookiesMatchingSearch() {
	var i, cookie, m = document.querySelectorAll(".jstree-search");
	var list = [];
	if( m && m.length > 0 ) {
		for(i = 0; i < m.length; i++) {
			cookie = _cookieData[parseInt(m[i].getAttribute("id"), 10)];
			if( cookie ) {
				// matched element may also be a folder (domain) - not a cookie so 'cookie' here might be null
				list.push(cookie);
			}
		}
	}
	return list;
}

function deleteCookiesMatchingSearch() {
	var i, list = getCookiesMatchingSearch();
	if( list && list.length > 0 ) {
		if( confirm("Do you really want to delete all cookies that matched search? (" + list.length + ")") ) {
			var count = 0, total = list.length;
			for(i = 0; i < list.length; i++) {
				removeCookie(list[i], function() {
					count++;
					if( count == total ) {
						loadCookieTree();
					}
				});
			}
		}
	}
	else {
		alertify.error("No cookies matching search!");
	}
}

function customMenu(node)
{
	var items = {};

	var type = node.li_attr.type;
	if( type == "domain" )
	{
		var domain = node.li_attr.id; // this is the actual cookie domain
		var childIds = $.merge([], node.children); // take a copy
		items.deleteAll = {
			"label": "Delete all cookies",
			"icon": "images/icon-clear-small.png",
			"action": function() {
				var j, tr = $("div#tree").jstree(true);
				for(j = 0; j < childIds.length; j++)
				{
					var id = parseInt(childIds[j], 10);
					var cookie = _cookieData[id];
					tr.delete_node(id + "");
					deleteCookie(cookie, function(c) {
						// console.log("Deleted", c);
					});
				}
				alertify.success("Deleted!");
			}
		};
		items.deleteSession = {
			"label": "Delete session cookies",
			"icon": "images/icon-clear-small.png",
			"action": function() {
				var j, tr = $("div#tree").jstree(true);
				for(j = 0; j < childIds.length; j++)
				{
					var id = parseInt(childIds[j], 10);
					var cookie = _cookieData[id];
					if( cookie.session )
					{
						tr.delete_node(id + "");
						deleteCookie(cookie, function(c) {
							// console.log("Deleted", c);
						});
					}
				}
				alertify.success("Deleted!");
				setCookieFormVisible(false);
			}
		};
		items.createCookie = {
			"label": "Create a cookie for this domain",
			"icon": "images/icon-add-small.png",
			"action": function() {
				showCookie(-1, {domain: domain});
				setCookieFormVisible(true);
				$("input.name").focus();
			}
		};
		items.whitelistDomain = {
			"label": "Whitelist domain",
			"action": function() {
				chrome.runtime.sendMessage({command: "whitelist", host: domain}, function(response) {
					alertify.success(getStarDomain(domain) + " whitelisted!");
				});
			}
		};
		items.blacklistDomain = {
			"label": "Blacklist domain",
			"action": function() {
				chrome.runtime.sendMessage({command: "blacklist", host: domain}, function(response) {
					alertify.success(getStarDomain(domain) + " blacklisted!");
				});
			}
		};
		items.exportDomain = {
			"label": "Export domain cookies",
			"action": function() {
				exportDomainCookies(domain);
			}
		};
	}
	else if( type == "cookie" )
	{
		var id = node.li_attr.id;
		var cookie = _cookieData[id];

		if( isCookieWhitelisted(cookie) )
		{
			items.unwhitelist = {
				"label": "Remove cookie from whitelist",
				"action": function() {
					chrome.runtime.sendMessage({command: "setwhitelisted", cookie: cookie, bool: false}, function(response) {
						alertify.success("Cookie " + cookie.name + " removed from cookie whitelist!");
						setCookieWhitelisted(cookie, false); // update local cache
						$("div#tree").jstree(true).set_icon(id, getIconFile(cookie));
					});
				}
			};
		}
		else
		{
			items.whitelist = {
				"label": "Add cookie to whitelist",
				"action": function() {
					chrome.runtime.sendMessage({command: "setwhitelisted", cookie: cookie, bool: true}, function(response) {
						alertify.success("Cookie " + cookie.name + " added to cookie whitelist!");
						setCookieWhitelisted(cookie, true); // update local cache
						$("div#tree").jstree(true).set_icon(id, getIconFile(cookie));
					});
				}
			};
		}

		if( isCookieBlacklisted(cookie) )
		{
			items.unblacklist = {
				"label": "Remove cookie from blacklist",
				"action": function() {
					chrome.runtime.sendMessage({command: "setblacklisted", cookie: cookie, bool: false}, function(response) {
						alertify.success("Cookie " + cookie.name + " removed from cookie blacklist!");
						setCookieBlacklisted(cookie, false); // update local cache
						$("div#tree").jstree(true).set_icon(id, getIconFile(cookie));
					});
				}
			};
		}
		else
		{
			items.blacklist = {
				"label": "Add cookie to blacklist",
				"action": function() {
					chrome.runtime.sendMessage({command: "setblacklisted", cookie: cookie, bool: true}, function(response) {
						alertify.success("Cookie " + cookie.name + " added to cookie blacklist!");
						setCookieBlacklisted(cookie, true); // update local cache
						$("div#tree").jstree(true).set_icon(id, getIconFile(cookie));
					});
				}
			};
		}


		items.deleteCookie = {
			"label": "Delete cookie",
			"icon": "images/icon-clear-small.png",
			"action": function() {
				$("div#tree").jstree(true).delete_node(id + "");
				deleteCookie(cookie, function(c) {
					// console.log("Deleted", c);
					alertify.success("Deleted!");
					setCookieFormVisible(false);
				});
			}
		};
	}
	return items;
}

function getTree()
{
	return $("div#tree").jstree(true);
}

function search()
{
	var s = $("input.search").val();
	$("div#tree").jstree(true).search(s);
	if( s && s != "" ) {
		document.title = "Cookiebro Editor - Search: " + s;
	}
	else {
		document.title = "Cookiebro Editor";
	}
	updateURL();
}

function getStarDomain(domain)
{
	if( domain && domain.length > 0 && domain.charAt(0) == '.' )
	{
		return "*" + domain;
	}
	else
	{
		return domain;
	}
}

function saveCookie(c, callback)
{
	var cookie = jQuery.extend(true, {}, c);

	cookie.url = (cookie.secure ? "https" : "http") + "://" + (cookie.domain.charAt(0) == '.' ? cookie.domain.substring(1) : cookie.domain) + cookie.path;
	if( cookie.hostOnly )
	{
		delete cookie["domain"];
	}
	delete cookie["hostOnly"];
	delete cookie["session"];
	// console.log("Setting", cookie);
	chrome.runtime.sendMessage({command: "createcookie", cookie: cookie}, callback);
}

function deleteCookie(cookie, callback)
{
	chrome.runtime.sendMessage({command: "deletecookie", cookie: cookie}, callback);
}

function getCookieForm()
{
	var cookie = {};
	cookie.domain = $("input.domain").val(); // sanitize
	cookie.name = $("input.name").val();
	cookie.value = $("input.value").val();
	cookie.path = $("input.path").val();
	cookie.secure = $("input.secure").prop('checked');
	cookie.session = $("input.session").prop('checked');
	if( !cookie.session && $("input.expires").val().trim() != "" )
	{
		cookie.expirationDate = moment($("input.expires").val()).toDate().getTime() / 1000;
	}
	cookie.httpOnly = $("input.httponly").prop('checked');
	cookie.hostOnly = $("input.hostonly").prop('checked');
	if( cookie.domain.length > 0 && cookie.domain.charAt(0) == '*' )
	{
		cookie.domain = cookie.domain.substring(1);
	}
	if( cookie.hostOnly && cookie.domain.length > 0 && cookie.domain.charAt(0) == '.' )
	{
		cookie.domain = cookie.domain.substring(1);
	}
	if( isFirstPartyIsolationSupported() )
	{
		cookie.firstPartyDomain = $("input.firstPartyDomain").val();
	}

	cookie.storeId = $("input.store").val();
	return cookie;
}

function showCookie(id, cookie)
{
	$("input.domain").val(cookie.domain);
	$("input.name").val(cookie.name);
	$("input.value").val(cookie.value);
	$("input.path").val(cookie.path);
	$("input.expires").val(cookie.expirationDate ? moment(cookie.expirationDate * 1000).format("YYYY-MM-DD HH:mm:ss") : "");
	$("input.secure").prop('checked', cookie.secure == true);
	$("input.session").prop('checked', cookie.session == true);
	$("input.httponly").prop('checked', cookie.httpOnly == true);
	$("input.hostonly").prop('checked', cookie.hostOnly == true);
	$("input.store").val(cookie.storeId);
	$("input.cookieId").val(id);
	if( isFirstPartyIsolationSupported() )
	{
		$("input.firstPartyDomain").val(cookie.firstPartyDomain);
		$("tr.firstPartyDomainRow").css({display: "table-row"});
	}

	if( id < 0 ) // create new
	{
		$("button.create").css({display: ""});
		$("button.update").css({display: "none"});
		$("button.exportcookie").css({display: "none"});
		$("button.delete").css({display: "none"});
	}
	else
	{
		$("button.create").css({display: "none"});
		$("button.update").css({display: ""});
		$("button.exportcookie").css({display: ""});
		$("button.delete").css({display: ""});
	}
	setCookieFormVisible(true);
}

function setCookieFormVisible(bool)
{
	$("div#cookie").css({display: bool ? "block" : "none"});
}

/**
 * @param json Cookies as JSON (text)
 */
function importCookies(json)
{
	chrome.runtime.sendMessage({command: "importcookies", data: json, storeId: _cookieStoreId}, function(response) {
		loadCookieTree();
		alertify.success("Cookies imported!");
	});
}

function exportCookies()
{
	chrome.runtime.sendMessage({command: "getallcookies", storeId: _cookieStoreId}, function(response) {
		var cookies = response.cookies;
		var json = JSON.stringify(cookies, null, 4);
		downloadFile(json, "cookies.json", "application/json");
		//alertify.success("Cookies exported!");
	});
}

function updateURL()
{
	var separator = "?";
	var title = "Cookiebro Editor";
	var search = $("input.search").val();
	var url = document.location.origin + document.location.pathname;

	if( _cookieStoreId != undefined ) {
		url += "?store=" + _cookieStoreId;
		separator = "&";
	}
	if( search != "" && search ) {
		url += separator + "search=" + encodeURIComponent(search);
		separator = "&";
	}
	if( _expanded ) {
		url += separator + "expand=true";
		separator = "&";
	}
	history.pushState({}, title, url);
}
