<!DOCTYPE html>
<html lang="en" ng-app="halicrime">

  <?php require_once('head.php'); ?>

  <body>
    <div id="app" ng-app="halicrime" ng-controller="MapController as mapCtrl">
      <header>
        <h1 id="site-title" class="text-center">halicrime</h1>    
      </header>
      <div class="container-fluid">
        <div class="row">
          <div class="col-xs-12">
            <p>Your subscription to crime alerts has been cancelled. You will no longer receive emails.</p>
            <a class="btn btn-primary" href="/">Back to Crime Map</a>
            
            
          
          </div>
          <!-- end .col-xs-12 -->
        </div>
        <!-- end .row -->
      </div>
      <!-- end .container-fluid -->
    </div>
    <!-- end #app -->
    
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
  </body>

</html>
