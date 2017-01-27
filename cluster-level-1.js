/*
    Method that attempt to get the required articles to the main article by
    getting the abstract links and possible relations between them. This way 
    we create clusters of linked components and vote for the cluster most
    representative link.
*/

var neo4j = require('node-neo4j');

//Connect to db
var db = new neo4j('http://neo4j:lucas@localhost:7474');


if(process.argv[2] == undefined)
    throw "No article specified.";

var articleTitle = process.argv[2]

var dbQuery = [
    'MATCH (n1:Article {title:"ARTICLE-TITLE"})-[l1:ConnectsTo]->(n2:Article)',
    'OPTIONAL MATCH (n2)-[l2:ConnectsTo]->(n3:Article)',
    'WHERE (n1)-[:ConnectsTo]->(n3)',
    'RETURN n2,l2,n3'
].join(" ").replace("ARTICLE-TITLE", articleTitle);


//Execute query
db.cypherQuery(dbQuery, function(err, result) {

    var resultData = result.data;

    // console.log(resultData.map(function(a) {
        
    //     a = a.map(function(b) {
    //         if(b && b.title)
    //             return b.title;
    //         return "";
    //     });

    //     return JSON.stringify(a);
    

    // }).join("\n\n"));


    var articleDict = {}
    var clusterArray = [];

    var clusterCounting = 0;

    //Feed article dict and clusters
    for(var i = 0; i < resultData.length; i++) {
        var n1 = resultData[i][0];
        var n2 = resultData[i][2];

        //Feed article dict and add a cluster to it
        if(articleDict[n1["_id"]] == undefined) {
            articleDict[n1["_id"]] = { title: n1["title"], cIndex: clusterArray.length }
            clusterArray.push(clusterArray.length); 
        }   

        //If no node2, proceed next iteration
        if(n2 == null)
            continue;

        //Add node 2 to the article dict and copy the node 1 cluster index
        if(articleDict[n2["_id"]] == undefined) {
            //Add same index of the node 1 cluster
            articleDict[n2["_id"]] = { title: n2["title"], cIndex: articleDict[n1["_id"]]['cIndex']}  
        } else { //If node 2 already exists, join clusters
            clusterArray[articleDict[n2["_id"]]['cIndex']] = clusterArray[articleDict[n1["_id"]]['cIndex']];
        }  



        // //Get the relation cluster index by trying get the node1 index, node2, and if none of them exists, create a new
        // //In the case, the next one will be the one with the index equal to the array length
        // var relationClusterIndex = articleDict[n1["_id"]]['cIndex'] || articleDict[n2["_id"]]['cIndex'] || clusterCounting++;

        // //Put all the index in the relation the same
        // articleDict[n1["_id"]]['cIndex'] = relationClusterIndex;
        // articleDict[n2["_id"]]['cIndex'] = relationClusterIndex;
    }

    var clusterDict = {}

    //Compute all the articles into the cluster dict
    for(var key in articleDict) {
        var art = articleDict[key];

        //Init current cluster index if has not been yet
        if(clusterDict[clusterArray[art['cIndex']]] == undefined)
            clusterDict[clusterArray[art['cIndex']]] = [];        
        
        clusterDict[clusterArray[art['cIndex']]].push(art);
    }


    // console.log(clusterArray);
    // console.log(articleDict);
    console.log(clusterDict);

    // console.log(resultData);

});