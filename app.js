var neo4j = require('node-neo4j');
var async = require('async');



//Connect to db
var db = new neo4j('http://neo4j:lucas@localhost:7474');

RegExp.escape = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\\\$&");
};


function getLinksFromArticle(article, callback) {
    var dbQuery = 'MATCH (n:Article)-[l:ConnectsTo]->(o:Article) WHERE n.title = "' + article + '" RETURN o';
    
    db.cypherQuery(dbQuery, function(err, result) {
    
        var resultData = result.data;

        callback(err, article, resultData.map(function(obj){return obj.title;}));
    });   
}



var articlesLinks = {}


// create a queue object with concurrency 2
var asyncQueue = async.queue(function(article, taskCallback) {
    
    getLinksFromArticle(article, function(err, article, links) {
        articlesLinks[article] = links;
        
        console.log("Added links of " + article)
        
//        for(var i = 0; i < links.length; i++) {
//            var link = links[i];
//            
//            //If the link has not yet been in the dict, push it to dict and function queue
//            if(articlesLinks[link] == undefined) {
//                articlesLinks[link] = [];
//                asyncQueue.push(link);
//            }                
//        }
        
        taskCallback();        
    });
    
}, 1);


var linksToCount = {};

// assign a callback
asyncQueue.drain = function() {
    console.log('All items have been processed');
    console.log('Counting links');
    
    for(var article in articlesLinks) {
        var links = articlesLinks[article];
        
        for(var i = 0; i < links.length; i++) {
            var link = links[i];
            
            if(linksToCount[link] == undefined)
                linksToCount[link] = 1;
            else
                linksToCount[link] += 1;            
        }        
    }
    
    var linksToCountArr = [];
    
    //Put them to an array
    for(var art in linksToCount) {
        linksToCountArr.push({
            art: art,
            count: linksToCount[art]
        });
    }
    
    //Sort it
    var sorted = linksToCountArr.sort(function(a, b){ return b.count - a.count; });
    
    
    for(var i = 0; i < sorted.length; i++)
        console.log(sorted[i]);
};





getLinksFromArticle(process.argv[2], function(err, article, links) {
    
    for(var i = 0; i < links.length; i++) {
        var link = links[i];

        asyncQueue.push(link);         
    }
    
});


//var dbQuery = 'MATCH (n:Article)-[l:ConnectsTo]->(o:Article) WHERE n.title =~ "(?i)calculus" RETURN n,l,o';
//
//db.cypherQuery(dbQuery, function(err, result) {
//    
//    var resultData = result.data;
//    
//    for(var i = 0; i < resultData.length; i++) {
//       console.log(JSON.stringify(resultData[i].map(function(obj) {
//           return obj;
//        if(obj.hasOwnProperty('title'))
//            return obj['title'];
//        
//        return "->";
//       })));
//        console.log("\n");
//    }
//});