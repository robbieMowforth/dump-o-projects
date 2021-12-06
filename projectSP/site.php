<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <h1>Holding Page NO INFO HERE PLEASE</h1>
    <?php
    echo substr('!stats HELLO',0,6);
    echo substr('!stats',0,5);
    echo substr('!stats',6);

    require 'includes/dbh.inc.php';

    $playerID = 'Robbie33';

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

    echo $spawnedStoreS;
    echo gettype($spawnedStoreS);
    ?>
  </body>
</html>
