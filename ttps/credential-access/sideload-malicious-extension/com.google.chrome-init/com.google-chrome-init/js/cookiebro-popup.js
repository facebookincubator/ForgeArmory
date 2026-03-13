/**
 * Cookiebro
 *
 * Advanced cookie manager WebExtension by Nodetics <nodetics@gmail.com>
 * All Rights Reserved (C)
 */
$(document).ready(function() {
	chrome.tabs.query({active: true, currentWindow: true}, function(arrayOfTabs) {
		var tab = arrayOfTabs[0];
		var cookieStoreId = tab.cookieStoreId || "0"; // WebKit based browsers don't have this, default to "0"

		var host = getHostFromUrl(tab.url);

		var tophost;
		var items = host.split(".");
		if( items.length > 1 ) // host can be localhost so check this
		{
			items.shift();
			tophost = items.join(".");
		}

		var param = "?store=" + cookieStoreId;

		chrome.runtime.sendMessage({command: "init", host: host, storeId: cookieStoreId}, function(response) {
			var matchingRules = response.matchingRules;

			var i, html = "<div class='menu'>";
			if( tab.url.indexOf("http") == 0 )
			{
				if( matchingRules.length > 0 )
				{
					for(i = 0; i < matchingRules.length; i++) {
						html += "<div class='menuItem removeHost' data-host='" + matchingRules[i].host + "'>Remove <span class='host'>" + matchingRules[i].display + "</span> from whitelist</div>";
					}
				}
				else
				{
					html += "<div class='menuItem addHost' data-host='" + host + "'>Add <span class='host'>" + host + "</span> to cookie whitelist</div>";
					html += "<div class='menuItem addHost' data-host='." + host + "'>Add <span class='host'>*." + host + "</span> to cookie whitelist</div>";
					if( tophost != undefined )
					{
						html += "<div class='menuItem addHost' data-host='." + tophost + "'>Add <span class='host'>*." + tophost + "</span> to cookie whitelist</div>";
					}
				}
			}
			if( response.unwanted > 0 ) {
				html += "<div class='menuItem' id='clear'>Clear unwanted cookies (" + response.unwanted + " out of " + response.total + ")</div>";
			}
			if( tab.url.indexOf("http") == 0 ) {
				// Firefox doesn't support domain specific indexedDB deletion yet
				html += "<div class='menuItem' id='cleartab' title='Deletes " + (isFirefox() ? "" : "IndexedDB, ") + "sessionStorage, localStorage, cacheStorage and Service Worker data of the current domain (does not clear cookies!)'>Clear <b>" + host + "</b> domain data</div>";
			}
			html += "<div class='menuItem' id='options'>Options</div>";
			html += "<div class='menuItem' id='editor'>Cookie Editor</div>";
			html += "<div class='menuItem' id='log'>Cookie Log</div>";
			html += "</div>";

			$("body").html(html);

			$("div.addHost").click(function() {
				var item = $(this);
				var ahost = item.attr("data-host");

				chrome.runtime.sendMessage({command: "whitelist", host: ahost}, function(response) {
					alertify.success("Added to whitelist successfully!");
					setTimeout(function() { window.close(); }, 2000);
				});
			});
			$("div.removeHost").click(function() {
				var item = $(this);
				var ahost = item.attr("data-host");

				chrome.runtime.sendMessage({command: "removewhite", host: ahost}, function(response) {
					alertify.success("Removed from whitelist successfully!");
					setTimeout(function() { window.close(); }, 2000);
				});
			});
			$("div#clear").click(function() {
				chrome.runtime.sendMessage({command: "purge", storeId: cookieStoreId}, function(response) {
					$("body").html("<div class='message'>Unwanted cookies purged!</div>");
				});
			});
			$("div#options").click(function() {
				openTab("Cookiebro Options", "options.html" + param);
			});
			$("div#editor").click(function() {
				openTab("Cookiebro Editor", "editor.html" + param);
			});
			$("div#log").click(function() {
				openTab("Cookiebro Log", "log.html");
			});
			$("div#cleartab").click(function() {
				chrome.tabs.query({currentWindow: true, active: true}, function (tabs) {
					var tab = tabs[0];
					chrome.tabs.executeScript(tab.id, {file: "js/cleartab.js"}, function() {
						if( chrome.runtime.lastError ) {
							alertify.error("Failed to clear data! " + chrome.runtime.lastError.message);
						}
						else {
							alertify.success("Domain data cleared!");
						}
					});
				});
			});
		});
	});
});

function openTab(title, url)
{
	chrome.tabs.query({title: title}, function(tabs) {
		if( tabs.length > 0)
		{
			// activate & reload the existing tab
			chrome.tabs.update(tabs[0].id, {active: true, url: url});
		}
		else
		{
			chrome.tabs.create({'url': url});
		}
		window.close();
	});
}

function isFirefox() {
	return navigator.userAgent && navigator.userAgent.indexOf("Firefox") != -1;
}
