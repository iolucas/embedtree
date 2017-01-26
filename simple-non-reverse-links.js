/*
    Method that attempt to get the required articles to the main article by
    getting the abstract links and removing the links that reference back to main article.
*/

var neo4j = require('node-neo4j');

//Connect to db
var db = new neo4j('http://neo4j:lucas@localhost:7474');


if(process.argv[2] == undefined)
    throw "No article specified.";

var articleTitle = process.argv[2]

var dbQuery = 'MATCH (n:Article {title:"'+ articleTitle + '"})-[:ConnectsTo]->(o:Article) WHERE NOT (o)-[:ConnectsTo]->(n) RETURN o';

//Execute query
db.cypherQuery(dbQuery, function(err, result) {

    var links = result.data.map(function(a){return a.title;});

    console.log(links.join("\n"));

    console.log("\n" + links.length + " links");
});