const videos = [
  document.querySelector('#tut1'),
  document.querySelector('#tut2'),
  document.querySelector('#tut3'),
];

const playButtons = [
  document.querySelector('#play1'),
  document.querySelector('#play2'),
  document.querySelector('#play3'),
];

const dialog = document.querySelector('#dlog');
const back = document.querySelector('#back');

const showVideo = (video, button) => {
  videos.forEach(v => v.style.display = 'none');
  video.style.display = 'block';
  video.play();
  dialog.showModal();
};

playButtons.forEach((button, index) => {
  button.addEventListener('click', () => showVideo(videos[index], button));
});

back.addEventListener('click', () => {
  videos.forEach(video => video.pause());
  dialog.close();
});
