// @ngInject
angular.module('flocs.instructions')
.directive('flocsInstructionArea', function($q, $timeout, instructionsService) {

  function setPlacementWatcher(scope, placementParams) {

    function setPlacement(placement) {
      scope.placementCss.left = placement.left + 'px';
      scope.placementCss.top = placement.top + 'px';
      scope.placementCss.width = placement.width + 'px';
      scope.placementCss.height = placement.height + 'px';
      //console.log('new placement:', scope.placementCss);
    }

    var selector = placementParams.selector;
    var isSvg = selector.indexOf('svg') > -1;
    var element = angular.element(document.querySelector(selector));
    var adjustPlacement = function(placement) {
      if (placementParams.offset) {
        placement.left += placementParams.offset.x;
        placement.top += placementParams.offset.y;
      }
      if (placementParams.size) {
        placement.width = placementParams.size.width;
        placement.height = placementParams.size.height;
      }
    };
    var getPlacement = null;
    if (isSvg) {
      getPlacement = function() {
        var bbox = element[0].getBBox();
        var placement = {
          left: bbox.x,
          top: bbox.y,
          width: bbox.width,
          height: bbox.height,
        };
        adjustPlacement(placement);
        return placement;
      };
    } else {
      getPlacement = function() {
        var position = element.position();
        var placement = {
          left: position.left,
          top: position.top,
          width: element.outerWidth(),
          height: element.outerHeight()
        };
        adjustPlacement(placement);
        return placement;
      };
    }
    scope.$watch(getPlacement, setPlacement, true);
  }

  return {
    restrict: 'E',
    scope: {
      key: '@',
      placement: '=',
      popoverPosition: '@',
    },
    templateUrl: 'instructions/instruction-area.tpl.html',
    link: function(scope, element, attrs) {
      var instructionSeen = null;
      scope.area = {
        visible: false
      };
      scope.placementCss = {
        left: '0',
        top: '0',
        width: '0',
        height: '0',
      };
      scope.instruction = {
        active: false,
        text: '',
        position: scope.popoverPosition || 'top',
      };

      scope.showing = function(instruction) {
        if (instructionSeen === null) {
          instructionSeen = $q.defer();
        }
        scope.instruction.text = instruction.text;
        scope.instruction.active = true;
        $timeout(function() {
          scope.area.visible = true;
        });
        setPlacementWatcher(scope, scope.placement);
        console.log('showing:', instruction);
        return instructionSeen.promise;
      };

      scope.close = function() {
        scope.area.visible = false;
        scope.instruction.active = false;
        if (instructionSeen !== null) {
          instructionSeen.resolve();
        }
      };

      instructionsService.registerInstructionArea(scope);
    }
  };
});
