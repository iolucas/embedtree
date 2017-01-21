var neo4j = require('node-neo4j');
var async = require('async');
var fs = require("fs");

//Connect to db
var db = new neo4j('http://neo4j:lucas@localhost:7474');

var article = process.argv[2];

var titleVar = "title";

var maxNumberOfTransverse = 4;

//Algorithm 

//Get page k most relevant transversal connections (i.e. k can be 10)
//check a few diferent values of k and how they behave

//Most relevant we say the most intersection in the level 2
//If the connection has no intersection, we may check level 3

//for each connection, checks:
    //If the owner of the connection is on it, remove it
    //get the tranversal connections for each one of them and checks
        //If it has the original article, this article is removed


//the left articles are consired to come "before" the original articles




getPageTranversal(article, function(textSorted) {

    var textBuffer = "";

    for(var i = 0; i < textSorted.length; i++) {
        //console.log((i + 1) + "/" + textSorted.length);
        console.log(textSorted[i].join(" - "));
        textBuffer += textSorted[i].join(" ") + "\r\n";
    }  

    fs.writeFileSync("buffer.txt", textBuffer, 'utf-8');  

});

function getPageTranversal(article, callback) {

    //Transverse database by 1, 2 and 3 levels
    //We must not skip any transversal level to ensure all the articles will be computed to the dict
    //And there will be no links point to undefined articles
    var dbQuery = 'MATCH (n:Article)-[l:ConnectsTo*1..3]->(o:Article) WHERE n.' + titleVar + ' = "' + article + '" RETURN n,l,o';

    var articleDict = {}
    var linkDict = {};


    //Execute query
    db.cypherQuery(dbQuery, function(err, result) {

        if(err) {
            console.log(err);
            process.exit();
        }

        var resultData = result.data;

        //Iterate thru the results
        for(var i = 0; i < resultData.length; i++) {
            var d = resultData[i];

            var source = d[0];
            var target = d[2];

            var links = d[1];

            for(var j = 0; j < links.length; j++) {
                var link = links[j];
                
                var linkLevel = j;
                
                var sourceId = link.start.substr(link.start.lastIndexOf("/") + 1);
                var targetId = link.end.substr(link.end.lastIndexOf("/") + 1);

                //Create link key to ensure it is unique
                var linkKey = sourceId + "-" + targetId;
                
                //If the links is not present or the current link level is higher than the new, add it
                if(linkDict[linkKey] == undefined || linkDict[linkKey][2] > linkLevel) {
                    linkDict[linkKey] = [sourceId, targetId, linkLevel]  
                }
            }
                    
            //Push articles to the dict
            articleDict[source["_id"]] = source[titleVar];
            articleDict[target["_id"]] = target[titleVar];
        }    

        var linkToCount = {}

        //Get links values
        for(var link in linkDict) {
            var targetArticleId = linkDict[link][1];
            var linkLevel = linkDict[link][2];

            //Init link to count obj if it is not
            if(linkToCount[targetArticleId] == undefined) {
                linkToCount[targetArticleId] = [];
                for(var m = 0; m < maxNumberOfTransverse; m++)
                    linkToCount[targetArticleId].push(0);   
            }
            
            //Push the link level to the link to count array
            linkToCount[targetArticleId][linkLevel] += 1;

    //        if(linkToCount[targetArticleId] == undefined) {
    //            if(level1Ids.indexOf(targetArticleId) != -1)
    //                linkToCount[targetArticleId] = 1;
    //            else
    //                linkToCount[targetArticleId] = 1
    //        } else {
    //            linkToCount[targetArticleId] += 1;
    //        } 
        }

        var linkToCountArr = [];

        //Convert the link count to array
        for(var art in linkToCount) {
            linkToCountArr.push({
                art: art,
                count: linkToCount[art]
            }); 
        }
        
        //Rank vector that specifies the importance order of the links
        var rankVectors = [
            [2,1,0,3],
            [1,0,2,3],
            [0,1,2,3]
        ]
        
        var rankVector = rankVectors[1];
        
        //Sort it
        var sorted = linkToCountArr.sort(function(a, b) { 

            var diff = 0;
            
            //Check the count values to sort correctly
            for(var m = 0; m < rankVector.length; m++) {
                var lookupIndex = rankVector[m];
                
                diff = b.count[lookupIndex] - a.count[lookupIndex];
                
                //If the diff is diferent from 0, stop iteration and return
                if(diff != 0)
                    break; 
                
                //If it is 0, proceed to the next level
            }
            
            return diff;    
        });

        var textSorted = sorted.map(function(a) {
            a.text = articleDict[a.art];
            return [a.art, articleDict[a.art], a.count];    
        });
        
        

        callback(textSorted);
        
    });   

}