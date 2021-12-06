<?php
  include_once 'includes/dbh.inc.php'; //include_once; the file is only included only once
  require_once 'includes/dbFuncs.php';
?>

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <form action="database.php" method="post">
      Enter DataTable: <input type="text" name="dataTable">
      Enter playerID: <input type="text" name="playerID">
      Enter zone: <input type="text" name="zone">
      Enter spawnedString: <input type="text" name="spawned">
      Enter collectedString: <input type="text" name="collected">
      <br>
      <!-- <a href="http://localhost/www/site.php" formtarget="_blank"> -->
      <input type="submit" name="populateData" value="Populate Data" onclick="location.href='http://localhost/www/site.php';">
      <!--</a>-->

      <!--TODO Need to figure out method to stop data being sent on refresh,
      low priority -->
    </form>
    <br>

    <?php
    if($_SERVER['REQUEST_METHOD'] == "POST" && isset($_POST['populateData'])){
        $runID = uniqid();
        $playerID = $_POST['playerID'];
        $zone = $_POST['zone'];
        $spawned = $_POST['spawned'];
        $collected = $_POST['collected'];
        $currDate = date("Y-m-d H:i:s");
        popButton($conn,$runID,$playerID,$zone,$spawned,$collected,$currDate);
    } else{"Couldn't get data";}
    ?>
    <br>
    <!-- Shows whats in the db -->
    <?php
      $sql = "SELECT *
              FROM spawnCatch;
              ";

      $result = mysqli_query($conn,$sql);
      $resultCheck = mysqli_num_rows($result); //error check to make sure we got data

      if ($resultCheck > 0){
        while($row = mysqli_fetch_assoc($result)){
          echo $row['playerID'] . "<br>";
        }
      } else{ echo "No Results Returned"; }
    ?>

  </body>
</html>
