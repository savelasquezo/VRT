var vrtv = document.getElementById("vrt-video");
var play = document.getElementById('play');
var back = document.getElementById('back');
var dlog = document.getElementById('dlog');

play.addEventListener('click', function() {
  vrtv.play();
  dlog.showModal();
});

back.addEventListener('click', function() {
  vrtv.pause();
  dlog.close();
});
