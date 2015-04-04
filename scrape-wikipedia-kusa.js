//scrape-wiki-kusa.js
var cclient = require('cheerio-httpcli');
var mongoose = require('mongoose');
var sleep = require('sleep');

var hostname = "https://ja.wikipedia.org";
var startpage = hostname + "/wiki/Category:%E8%8D%89";
var dbConStr = 'mongodb://localhost/kusa';

function initDBCon() {
	mongoose.connect(dbConStr);

	process.on('SIGINT', function() {
		mongoose.disconnect();
	});
}

function getContentsSourcesModel() {
	var ContentsSourcesSchema = new mongoose.Schema({
		source_name: {
			type: String
		}
	});

	return mongoose.model('ContentsSources', ContentsSourcesSchema);
}

function getContentsModel() {
	var ContentsSchema = new mongoose.Schema({
		sources_id: ObjectId,
		url: {
			type: String
		},
		title: {
			type: String
		},
		body_text: {
			type: String
		},
		image: {
			data: Buffer,
			content_type: String
		}
	});

	return mongoose.model('Contents', ContentsSchema);
}

function parseWiki(url, title) {
	sleep.sleep(5);
	cclient.fetch(url, {}, function(err, $, res, body) {
		if (err) {
			console.log('error: ' + url + " - " + err);
			return;
		}
		if (res.statusCode != 200) {
			console.log('RC=' + res.statusCode + ' from ' + url);
			return;
		}

		var contentsSources = getContentsSourcesModel();
		var sourceObj = new contentsSources({
			source_name: hostname
		});

		var source_id = null;

		console.log('sourceObj=' + sourceObj);
		sourceObj.find({
			source_name: hostname
		}, function(err, docs) {
			if (err) {
				console.log('error: ' + err);
				return;
			}

			if (docs.length != 0) {
				console.log('found ' + hostname);
				source_id = docs[0]._id;
				return;
			}

			sourceObj.save(function(err, doc) {
				if (err) {
					console.log('err ' + err);
					return;
				}
				source_id = doc._id;
			});

			var contents = getContentsModel();
			var kusa = {};
			kusa.source_id = source_id;
			kusa.url = url;
			kusa.title = title;
			kusa.body_text = $('body').text();
			var kusaObj = new contents(kusa);
			kusaObj.save(function(err, doc) {
				if (err) {
					console.log('error: ' + err);
					return;
				}
				console.log('saved kusa.');
			});
		});
	});
};

initDBCon();
cclient.fetch(startpage, {}, function(err, $, res, body) {
	if (err) {
		console.log('error:' + startpage + " - " + err);
		return;
	}
	if (res.statusCode != 200) {
		console.log('RC=' + res.statusCode + ' from ' + url);
		return;
	}

	$('div#mw-pages div.mw-category a').each(function(idx) {
		var title = $(this).attr('title');
		var url = hostname + $(this).attr('href');
		console.log('kusa[' + idx + '] ' + title + ' ' + url);
		parseWiki(url, title);
	});
});
