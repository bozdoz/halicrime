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
            <p>Get notified when crime happens in your neighbourhood.</p>
            <p>Change the size of the zone using this slider and click or drag on the map to re-position the zone.</p>
            <div id="radius-field">
                <label for="radius">Area Size</label>
                <input type="range" name="radius" id="radius" min="200" max="10000" ng-model="mapCtrl.radius" ng-change="mapCtrl.setRadius(mapCtrl.radius)">
            </div>
         
            <div id="map-canvas"></div>
            
            <div ng-controller="SubscriptionController as subCtrl">
                
                <form id="subscription_form" name="subscription_form" novalidate ng-submit="subscription_form.$valid && subCtrl.subscribe(mapCtrl.region)">
                    
                    <div class="col-lg-6">
                      <div class="input-group">
                        <input placeholder="Email address" class="form-control" type="email" required name="email" ng-model="subCtrl.form.email" value="" ng-model-options="{ updateOn: 'default blur', debounce: { default: 500, blur: 0 } }">
                        <span class="input-group-btn">
                          <button class="btn btn-primary" ng-disabled="!subscription_form.$valid">Subscribe to Alerts</button>
                        </span>
                      </div>
                    </div>
                    
                    <span class="validation_error" ng-show="subscription_form.$dirty && !subscription_form.email.$valid">Please enter a valid email address.</span>
                </form>
                
                <p class="success" ng-show="subCtrl.isStage('confirm')">We have sent you an email to confirm your subscription. Please click the activation link inside.</p>
                <p class="error" ng-show="subCtrl.isStage('subscribe_error')">There was an error subscribing you.</p>
                
            </div>
            
          
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
