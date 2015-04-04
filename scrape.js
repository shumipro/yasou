var cclient = require('cheerio-httpcli');
var sleep = require('sleep');

var hostname = "http://kasugak.sakura.ne.jp";

function parseComment(url) {
	// console.log("comment: " + url);
	cclient.fetch(url, {}, function(err, $, res, body) {
		if (err) {
			console.log('error:' + url + " - " + err);
			return;
		}
		if (res.statusCode != 200) {
			console.log('RC=' + res.statusCode + ' from ' + url);
			return;
		}

		// pase data and push it to DB.
		var children = $('body div table td').children();
		var current = children.first();
		while (current != null && current != undefined) {
			console.log("data:" + current.data);
			current = current.next();
		}
		// for (var i=0; i< children.length; i++) {
			// console.log(children.get(i).text());
			// console.log('child : ' + children.get(i).text());
		// }
		// var texts = $('td').text().split('[\s　]');
		// for (var i =0; i < texts.length; i++ ) {
		// 	console.log('text:' +texts[i] );
		// }
	});
}

function parseKsgk( /* string */ url) {
	// console.log("parsing: " + url);
	cclient.fetch(url, {}, function(err, $, res, body) {
				if (err) {
			console.log('error:' + url + " - " + err);
			return;
		}
		if (res.statusCode != 200) {
			console.log('RC=' + res.statusCode + ' from ' + url);
			return;
		}

		$('table a').each(function(idx) {
			var page = hostname + "/" + $(this).attr('href');
			// sleep.sleep(1);
			if (page.indexOf("/comment/") != -1) {
				parseComment(page);
			} else {
				parseKsgk(page);
			}
		});
	});
}

parseKsgk(hostname + '/abckamei.html');