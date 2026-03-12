/* jshint ignore:start */
(async function() {
	if( window.localStorage && window.localStorage.length > 0 ) {
		try {
			window.localStorage.clear();
			console.log("localStorage cleared");
		}
		catch(e) {
			console.log("Failed to clear localStorage", e);
		}
	}
	if( window.sessionStorage && window.sessionStorage.length > 0 ) {
		try {
			window.sessionStorage.clear();
			console.log("sessionStorage cleared");
		}
		catch(e) {
			console.log("Failed to clear sessionStorage", e);
		}
	}
	if( window.caches ) {
		try {
			var keys = await caches.keys();
			await Promise.all(keys.map(async key => {
				try {
					await caches.delete(key);
					console.log("Deleted cache with key " + key);
				}
				catch(ex) {
					console.log("Failed to remove cache " + key, ex);
				}
			}));
		}
		catch(e) {
			console.log("Failed to remove caches", e);
		}
	}
	try {
		if( window.indexedDB && window.indexedDB.databases ) {
			window.indexedDB.databases().then(function(r) {
				for (var i = 0; i < r.length; i++) {
					window.indexedDB.deleteDatabase(r[i].name);
					console.log("Deleted indexedDB with name " + r[i].name);
				}
			});
		}
		else {
			// databases() isn't supported in Firefox yet. @see https://bugzilla.mozilla.org/show_bug.cgi?id=934640
			console.log("IndexedDB databases cannot be removed because indexedDB.databases() function is not supported by this browser");
		}
	}
	catch(e) {
		console.log("Unable to remove indexedDB databases", e);
	}
	
	if( navigator.serviceWorker ) {
		try {
			var workers = await navigator.serviceWorker.getRegistrations();
			var workerCount = 0;
			await Promise.all(workers.map(async worker => {
				try {
					await worker.unregister();
					workerCount++;
				}
				catch(ex) {
					console.log("Failed to remove Service Worker", ex);
				}
			}));
			if( workerCount > 0 ) {
				console.log("Service Workers removed (" + workerCount + ")");
			}
		}
		catch(e) {
			console.log("Failed to remove Service Workers", e);
		}
	}
	window.name = ""; // block tracking using window.name as cross-site storage: https://en.wikipedia.org/wiki/HTTP_cookie#%22window.name%22_DOM_property
	console.log("Data cleanup complete.");
})();
/* jshint ignore:end */
