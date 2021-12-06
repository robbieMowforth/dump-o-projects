<?php
//Function populates data based on user entry though site (database.php)
function popButton($conn,$runID,$playerID,$zone,$spawned,$collected,$date){
  /* Prepared statement, stage 1: prepare */
  $stmt = $conn->prepare("INSERT INTO spawnCatch(
    runID,
    playerID,
    zone,
    spawned,
    collected,
    date_time) values (?,?,?,?,?,?)
  ");

  /* Prepared statement, stage 2: bind and execute */
  // "is" means that $id is bound as an integer and $label as a string
  // https://www.php.net/manual/en/mysqli-stmt.bind-param.php
  $stmt->bind_param("ssssss", $runID,
                          $playerID,
                          $zone,
                          $spawned,
                          $collected,
                          $date);

  $stmt->execute();
}

/*This function is checking the spawnCatch table and then updating the playerCollections
table with the newly updated collection string found.
TODO:
  - Add in a check that if no new records for playerID, don't run SQL stmt (use date_time) CHECK
*/
function collectionUpdate($conn){
  //where we store variables such as a full list of all items etc


  //This is selecting all spawned/collected items per playerID in the spawnCatch table
  $sql = "SELECT playerID,
            group_concat(spawned) as spawnedC,
            group_concat(collected) as collectedC
          FROM spawnCatch
          WHERE DATE(date_time) = CURDATE()
          GROUP BY playerID;
          ";
 $result = mysqli_query($conn,$sql);
 $resultCheck = mysqli_num_rows($result); //error check to make sure we got data

 //loops though each row of the $sql query results
 if ($resultCheck > 0){
   while($row = mysqli_fetch_assoc($result)){
     //takes the all collected/spawned items per player and puts into arrays
     $pIDArrS = explode(',',$row['spawnedC']);
     $pIDArrC = explode(',',$row['collectedC']);


     /*
     the statement below is used to fetch any spawned/collection string already stored for the
     playerID of the current row.
     */
     $stmt = $conn->prepare("SELECT spawned, collected
       FROM playerCollections
       WHERE playerID =?;
     ");

     $stmt->bind_param("s", $row['playerID']);

     $stmt->execute();
     $stmt->store_result();
     $stmt->bind_result($spawnedStore,$collectedStore);
     $stmt->fetch();

     /*
     here we are mergiging the spawned string from the store in the table
     with the collection string from the spawnCatch table
     */
     if($spawnedStore === NULL){
       $uniArrS = array_unique($pIDArrS);
     } else{
       $spwnArr = explode(',',$spawnedStore);
       $newSpwnArr = array_merge($pIDArrS,$spwnArr);

       $uniArrS = array_unique($newSpwnArr);
     }
     /*
     here we are mergiging the collection string from the store in the table
     with the collection string from the spawnCatch table
     */
     if($collectedStore === NULL){
       $uniArrC = array_unique($pIDArrC);
     } else{
       $collArr = explode(',',$collectedStore);
       $newCollArr = array_merge($pIDArrC,$collArr);

       $uniArrC = array_unique($newCollArr);
     }

     //takes our merged output and truns it back into a comma delimited string
     $uniArrStrS = implode(',',$uniArrS);
     $uniArrStrC = implode(',',$uniArrC);

     //calculates the completion rate of items for the player
     $complRate = completionRate($uniArrC);

     /*
     This statement is populating the playerCollections table with the newley made collection
     string.
     */
     $mergeStmt = $conn->prepare("INSERT INTO playerCollections (playerID,spawned,collected)
     VALUES (?,?,?)
     ON DUPLICATE KEY UPDATE spawned=?, collected=?;

     ");

     $mergeStmt->bind_param("sssss", $row['playerID'],
                                $uniArrStrS,
                                $uniArrStrC,
                                $uniArrStrS,
                                $uniArrStrC);

     $mergeStmt->execute();

     //echoing out the data
     echo "PlayerID: " . $row['playerID'] . "<br>" .
          "SpawnedC: " . $uniArrStrS . "<br>" .
          "CollectedC: " . $uniArrStrC . "<br>" .
          "CompletionRate: " . $complRate;

   }
 } else{ echo "No Results Returned"; }
}

/*
Fucntion that gets the count of a set item within the spawnCatch mysql_list_tables
TODO:
  - remove the comma from the end of the string list print
  - add a loop to print the count per day and report back
*/
function itemCounter($conn,$itemName,$startDate,$endDate){
  $stmt = $conn->prepare("SELECT date(date_time),
                            group_concat(spawned) as spawnedC,
                            group_concat(collected) as collectedC
    FROM spawnCatch
    WHERE date(date_time) >= ? AND date(date_time) <= ?
    GROUP BY date(date_time);
  ");

  $stmt->bind_param("ss",$startDate,$endDate);

  $stmt->execute();
  $stmt->store_result();
  $stmt->bind_result($date,$spawnedStore,$collectedStore);

  $spwnArr = array();
  $collArr = array();
  $spwnCount = 0;
  $collCount = 0;

  while($stmt->fetch()){
    $spwnArr = explode(',',$spawnedStore);
    $collArr = explode(',',$collectedStore);
    echo "<br><br>Spawned String: ";

    foreach($spwnArr as $i){
      echo $i . ", ";
      $spwnCount += ($i === $itemName) ? 1 : 0;
    }
    echo "<br>Collected String: ";
    foreach($collArr as $i){
      echo $i . ", ";
      $collCount += ($i === $itemName) ? 1 : 0;
    }
  }

  echo "<br>The Item Name: " . $itemName;
  echo "<br>Spawn Count: " . $spwnCount . "<br>Collection Count: " . $collCount;



}

//This fucntion gets the spawned string for certain playerID
/*TODO:
- Look at making a more object orienteated approach using these fucntions (see userObj.php)
*/
function getCollection($conn,$playerID){
  $stmt = $conn->prepare("SELECT spawned, collected
    FROM playerCollections
    WHERE playerID =?;
  ");

  $stmt->bind_param("s", $playerID);

  //$result = mysqli_query($conn,$stmt);
  //$resultCheck = mysqli_num_rows($result);

  $stmt->execute();
  $stmt->store_result();
  $stmt->bind_result($spawnedStoreS,$collectedStoreS);
  $stmt->fetch();

  $spnArr = explode(',',$spawnedStoreS);

  return $spawnedStoreS;
}

//This function handles calculation of the completion of colection
function completionRate($pArray){
  require 'varStore.php';
  return $complRate = count($pArray) / count($fullCollection);
}

/*
TODO:
 - Need to link the varStore to the google sheet storage somehow
 - consider the larger implications of storage size and server calls made (SQL)
*/
