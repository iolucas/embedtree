/*
    Method that attempt to get the required articles to the main article by
    only getting the abstract links of the main article.
*/

var neo4j = require('node-neo4j');

//Connect to db
var db = new neo4j('http://neo4j:lucas@localhost:7474');


if(process.argv[2] == undefined)
    throw "No article specified.";

var articleTitle = process.argv[2]

var dbQuery = 'MATCH (:Article {title:"'+ articleTitle + '"})-[:ConnectsTo]->(o:Article) RETURN o';

//Execute query
db.cypherQuery(dbQuery, function(err, result) {

    var links = result.data.map(function(a){return a.title;});

    console.log(links.join("\n"));

    console.log("\n" + links.length + " links");
});