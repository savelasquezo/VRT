$(document).ready(function() {
    
    //$(".dial").knob();
    $('.dial').knob({
      'min':0,
      'max':100,
      'width':250,
      'height':250,
      'angleArc': 180,
      'angleOffset': -90,
      'textY': -20,
      'displayInput':true,
      'fgColor':"#17570e",
      'inputColor':"#292c2f",
      'release':function(v) {$("p");},
      'readOnly':true
    });
  });

  