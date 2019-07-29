let video, loop, angleEl;

(function() {
  main();
})();

async function main() {

  video = document.getElementById('inputVideo');
  angleEl = document.getElementById('angle');

  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
      .then(stream => {
        video.srcObject = stream;
      })
      .catch(err => {
        console.error(err)
      })
  } else {
    // unsupported or no camera

  }

  loop = setInterval(() => {

      // Copying the image in a temporary canvas
      let temp = document.createElement('canvas');

      temp.width  = video.offsetWidth;
      temp.height = video.offsetHeight;

      let tempcontext = temp.getContext("2d"),
          tempScale = (temp.height/temp.width);

      temp.drawImage(
          video,
          0, 0,
          video.offsetWidth, video.offsetHeight
      );

      url = temp.toDataURL('image/jpeg').split(',')[1];

      let fetch_data = {
        method: 'POST',
        body: {
          img: url
        },
        headers = new Headers()
      }

      req = await fetch('/tiltpy', fetch_data).then(async (res) => {
        if (res == 'recterror') {
          angleEl.innerText = 'Multiple faces detected. Please ensure that only you are being captured by your webcam or try changing the background.'
        } else {
          angleEl.innerText = res;
        }
      })

  }, 1000/30)

}

function stop() {
  let stream = video.srcObject;
  let tracks = stream.getTracks();

  for (track of tracks) {
    track.stop();
  }

  video.srcObject = null;
}

function requestpy(options) {
  return new Promise ((resolve, reject) => {
    let req = http.request(options);

    req.on('response', res => resolve(res));
    req.on('error', err => reject(err));
  })
}