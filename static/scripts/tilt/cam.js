let video, loop, angleEl;
let left, right, leftEl, rightEl;

$(document).ready(() => {
  $('.main').hide()
  $('.start').click(main)
})

async function main() {

  $('.splash').fadeOut(500, () => {
    $('.main').fadeIn(500);
  });

  video = document.getElementById('inputVideo');
  angleEl = document.getElementById('angle');

  leftEl = document.getElementById('max-angle-txt');
  rightEl = document.getElementById('min-angle-txt');

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

  loop = setInterval(async () => {

      // Copying the image in a temporary canvas
      let temp = document.createElement('canvas');

      temp.width  = video.offsetWidth;
      temp.height = video.offsetHeight;

      let tempcontext = temp.getContext("2d"),
          tempScale = (temp.height/temp.width);

      tempcontext.drawImage(
          video,
          0, 0,
          video.offsetWidth, video.offsetHeight
      );

      url = temp.toDataURL('image/jpeg').split(',')[1];

      body_data = {
        img: url
      }

      let fetch_data = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(body_data)
      }

      let res = await fetch('/tiltpy', fetch_data)
        .then(res => res.json())
        .then(data => {

          let res = data.res;

          if (res == 'faceerror0') {
            angleEl.innerText = 'No faces could be detected. Please ensure that your face is being captured by your webcam or try changing the background.'
          } else if (res == 'faceerror1') {
            angleEl.innerText = 'Multiple faces detected. Please ensure that only you are being captured by your webcam or try changing the background.'
          } else {

            angleEl.innerText = res;

            // left is -ve (min); right is +ve (max)
            if (res > right) {
              rightEl.innerText = res;
            } else if (left < min) {
              leftEl.innerText = res;
            }

          }

        })
        .catch(error => console.error(error))
      
  }, 1000/10);

}

function stop() {
  let stream = video.srcObject;
  let tracks = stream.getTracks();

  for (track of tracks) {
    track.stop();
  }

  video.srcObject = null;
}