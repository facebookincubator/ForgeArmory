/**
 * Cookiebro
 *
 * Advanced cookie manager WebExtension by Nodetics <nodetics@gmail.com>
 * All Rights Reserved (C)
 */
$(document).ready(function() {
	init();
});

var _logData;
var _whitelistedCookies;

function init()
{
	chrome.runtime.sendMessage({command: "getlog"}, function(response) {
		var log = response.log;
		var settings = response.settings;
		var i, row, html = "<table class='log'><thead><tr><th class='row'>Row</th><th class='date'>Event Timestamp</th><th class='domainIcon'></th><th class='domain'>Domain</th><th class='icon'></th><th class='name'>Name</th><th class='decision'>Decision</th><th class='actions'>Actions</th></tr></thead><tbody>";
		
		_logData = log;
		_whitelistedCookies = response.whitelistedCookies;
		
		if( log && log.length > 0 )
		{
			for(i = 0; i < log.length; i++)
			{
				row = log[i];
				if( row )
				{
					html += "<tr><td align='right'>" + (i + 1) + ".</td><td>" + moment(row.time).format("YYYY-MM-DD HH:mm:ss") + "</td>" + 
								"<td class='domainIcon'><img src='" + (settings.disablefavicons ? "images/site.png" : getDomainIcon(row.cookie.domain)) + "'></td>" +
								"<td class='domain'>" + row.cookie.domain + "</td>" +
								"<td class='cookieIcon'><img src='" + getIconFile(row.cookie) + "'></td>" +
								"<td class='cookieName'>" + row.cookie.name + "</td>" +
								"<td class='decision'><span class='decision " + row.action + "'>" + row.action + "</span></td>" +
								"<td class='actions' data-row='" + i + "'>" + 
									"<span class='action whitelist' title='Allow all cookies from this domain'>Whitelist Domain</span>" +
									"<span class='action whitelistCookie' title='Whitelist this single cookie without whitelisting the whole domain'>Whitelist Cookie</span>";
					html += "<span class='action blacklist' title='Block all cookies from this domain'>Blacklist Domain</span>";
					html += "<span class='action blacklistcookie' title='Block this particular cookie'>Blacklist Cookie</span>";
					if( row.action != "Block" )
					{
						html += "<span class='action deletecookie'>Delete Cookie</span>";
					}	
					html += "</td></tr>";
				}
			}
			html += "</tbody></table>";
			
			$("#clearlog").click(function(evt) {
				chrome.runtime.sendMessage({command: "clearlog"}, function(response) {
					alertify.success("Cookie Log cleared!");
					$("div#cookielog").html("<center>No log entries yet!</center>");
					$("#clearlog").css("display", "none");
				});	
			});
		}
		else
		{
			html = "<center>No log entries yet!</center>";
			$("#clearlog").css("display", "none");
		}
		$("div#cookielog").html(html);
		$("span.action").click(function(e) {
			var button = $(this);
			var checkbox = button.parent().find("input");
			var rowId = parseInt(button.parent().attr("data-row"), 10);
			var data = _logData[rowId];
			console.log(data.cookie);

			if( button.hasClass("whitelist") )
			{	
				chrome.runtime.sendMessage({command: "whitelist", host: data.cookie.domain}, function(response) {
					alertify.success("Domain " + data.cookie.domain + " whitelisted!");
				});	
			}
			else if( button.hasClass("whitelistCookie") )
			{				
				chrome.runtime.sendMessage({command: "setwhitelisted", cookie: data.cookie, bool: true}, function(response) {
					alertify.success("Cookie " + data.cookie.name + " whitelisted!");
				});		
			}
			else if( button.hasClass("blacklist") )
			{				
				chrome.runtime.sendMessage({command: "blacklist", host: data.cookie.domain}, function(response) {
					alertify.success("Domain " + data.cookie.domain + " blacklisted!");
				});		
			}
			else if( button.hasClass("blacklistcookie") )
			{	
				chrome.runtime.sendMessage({command: "setblacklisted", cookie: data.cookie, bool: true}, function(response) {
					alertify.success("Cookie " + data.cookie.name + " blacklisted!");
				});		
			}
			else if( button.hasClass("deletecookie") )
			{				
				chrome.runtime.sendMessage({command: "deletecookie", cookie: data.cookie}, function(response) {
					alertify.success("Cookie deleted!");
				});		
			}
		});
	});
}
