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
    <h1>Collection Storage, Currently Daily Rotation for Checking</h1>
    <?php
    collectionUpdate($conn);
    itemCounter($conn,'c023','2021-01-01','2021-08-11');
    itemCounter($conn,'r044','2021-01-01','2021-08-11');
    ?>

  </body>
</html>
