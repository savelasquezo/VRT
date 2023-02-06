var progressBar = new ProgressBar.Line('#progress-bar', {
    strokeWidth: 2,
    easing: 'easeInOut',
    duration: 1400,
    color: '#FFEA82',
    trailColor: '#eee',
    trailWidth: 2,
    
    svgStyle: {width: '100%', height: '100%'},
    from: { color: '#184d5f', width: 2 },
    to: { color: '#0B5916', width: 3 },
    step: function(state, circle) {
      circle.path.setAttribute('stroke', state.color);
      circle.path.setAttribute('stroke-width', state.width);
    }
  });
  
progressBar.animate(bar_percent/100);
