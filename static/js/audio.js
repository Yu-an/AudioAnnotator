var play = function() {
  var audio = document.getElementById('audio1');
  if (audio.paused) {
    audio.play();
  } else {
    audio.pause();
    audio.currentTime = 0
  }
}

var btn = document.getElementById('play');
btn.onclick = play;