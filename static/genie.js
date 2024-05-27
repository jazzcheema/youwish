"use strict";

const WISH_API_ENDPOINT = '/wish';
const SEND_FAVORITE = '/favorite_video';
const $box = $('#box');
const $box2 = $('#box2');
const $box3 = $('#box3');
const $box4 = $('#box4');
const $box5 = $('#box5');


/**
 * Event for moving splash page Genie full body image--> follows mouse.
 */
function moveGenie(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = y * 180;
  const rotationY = x * 180;

  $box.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);
  playHomePageSound();
};




/**
 * Event for moving Login page Genie Head image--> follows mouse.
 */
function moveGenie2(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = y * 60;
  const rotationY = x * 60;

  $box2.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);

};




/**
 * Event for moving Carpet on signup page--> follows mouse.
 */
function moveCarpet(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = y * 60;
  const rotationY = x * 60;

  $box5.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);
};





/**
 * Event for moving final genie--> follows mouse.
 */
function moveFinalGenie(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = y * 120;
  const rotationY = x * 120;

  $box4.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);

};



/**
 * Event for moving lamp page on wish page--> follows mouse.
 */
function moveLamp(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = -y * 100;
  const rotationY = -x * 100;

  $box3.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);

};


/////////////////////////////////////////////////////////////////////////SOUNDS
//Play music for homepage.
function playHomePageSound() {
  const homePageSound = document.getElementById('homePageSound');
  if (homePageSound) {
    homePageSound.play();
  }
}



//Home Page Sound Ok
function homepageOk() {
  const loginHomeSndOk = document.getElementById('okSoundSplash');
  if (loginHomeSndOk) {
    setTimeout(() => {
      window.location.href = '/login';
    }, 400);
    loginHomeSndOk.play();
  }
}



//Genie Face Sound
function thwompSound() {
  const genieYellSound = document.getElementById('thwompSnd');
  if (genieYellSound) {
    genieYellSound.play();
  }
}



//Login Page Sound Ok
function loginSound() {
  const loginSndOk = document.getElementById('okSoundLogin');
  if (loginSndOk) {
    loginSndOk.play();
  }
}



//Forgot Password Sound
function forgotSound() {
  const forgotSnd = document.getElementById('forgotPasswordSnd');
  if (forgotSnd) {
    setTimeout(() => {
      window.location.href = '/forgot';
    }, 200);
    forgotSnd.play();
  }
}




//Forgot Password Send Sound
function forgotSendSound() {
  const sendForgotSnd = document.getElementById('forgotPasswordSendSnd');
  if (sendForgotSnd) {
    sendForgotSnd.play();
  }
}



//Signup Homepage Sound
function signupSndSplash() {
  const splashSignupSound = document.getElementById('signupSplashSound');
  if (splashSignupSound) {
    setTimeout(() => {
      window.location.href = '/signup';
    }, 300);
    splashSignupSound.play();
  }
}




//Signup Page Sound
function signupSnd() {
  const signupSndSubmit = document.getElementById('signupPageSnd');
  if (signupSndSubmit) {
    signupSndSubmit.play();
  }
}




//Magic Lamp Wish Sound
function magicLampSnd() {
  const lampWishSnd = document.getElementById('genieLampSnd');
  if (lampWishSnd) {
    lampWishSnd.play();
  }
}



//Home Button Nav Sound
function homeButtonSound() {
  const homeSnd = document.getElementById('homeButtonSnd');
  if (homeSnd) {
    setTimeout(() => {
      window.location.href = '/';
    }, 500);
    homeSnd.play();
  }
}




//Edit Profile Sound
function editProfileSound() {
  const editSnd = document.getElementById('editProfileSnd');
  if (editSnd) {
    editSnd.play();
  }
}




//Genie Page Music
$(document).ready(function () {
  const genieSnd = document.getElementById('geniePageSnd');
  if (genieSnd) {
    genieSnd.play();
  }
});


//Adds video to webcam div
function addWebCam() {
  return $(`
  <video id="video" autoplay></video>
  `);
}

/** Genie Final Face Sound w/ Webcam -> change background of container
 *  to control the missing background when video is added.
 */
async function genieLaughSound() {
  const genieFinalLaughSound = document.getElementById('genieLaughSnd');
  genieFinalLaughSound.volume = 0.4;
  if (genieFinalLaughSound) {
    genieFinalLaughSound.play();
  }
  $('#video-webcam-container').css({
    'opacity': '1',
    'width': '100%',
    'height': '100vh',
    'background-size': 'cover',
    'background-position': 'center',
    'background-image': 'url(/static/images/genie_background.gif)'
  }).append(addWebCam);

  const videoElement = document.getElementById('video');
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  videoElement.srcObject = stream;
}



//Genie page--> button appears to exit when his face is clicked.
function genieLaughAndExitButton() {
  setTimeout(() => {
    const genieHomeButton = $('<button>').text('Exit').addClass('genie-exit-button');
    genieHomeButton.on('click', function () {
      window.location.href = '/';
    });
    $('#genie-button').append(genieHomeButton);
  }, 4000);
}





//Ensure DOM is loaded before JS.
$(document).ready(function () {

  $('#box4').on('click', genieLaughAndExitButton);

  $('#box4').on('click', genieLaughSound);

  $('#edit-user-button').on('click', editProfileSound);

  $('#nav-bar-home').on('click', homeButtonSound);

  $('#magic-lamp-graphic').on('click', magicLampSnd);

  $('#signup-button').on('click', signupSnd);

  $('#signup-button-on-splash').on('click', signupSndSplash);

  $("#forgot-password-button").on('click', forgotSendSound);

  $("#login-button-on-splash").on('click', homepageOk);

  $('#box2').on('click', thwompSound);

  $("#login-button-page").on('click', loginSound);

  $("#forgot-button-page").on('click', forgotSound);

  //event for moving wish lamp.
  $(document).on('mousemove', moveLamp);

  //Event for moving final genie.
  $(document).on('mousemove', moveFinalGenie);

  //Event for moving carpet.
  $(document).on('mousemove', moveCarpet);

  //Event for moving login genie.
  $(document).on('mousemove', moveGenie2);

  //Event for moving homepage genie.
  $(document).on('mousemove', moveGenie);


});


///////////////////////////////////////////////////////////////////////////////
/**
 * Creates HTML for each Video display. This is wrapped inside a 'form' with
 * hidden_tag() already rendered on the page.
 */
function generateHtmlMarkup(video) {
  return $(`
    <ul>

        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/${video.id}?controls=0&showinfo=0&modestbranding=1"
        frameborder="0" allowfullscreen>
        </iframe>
        <div id="favorite-button-container">
        <p id="video-views-display">Views: ${video.views}</p>
          <button
          id="favorite-button"
          data-id="${video.id}"
          type="submit"><i id="video-favorite-display" class="bi bi-heart"></i></button>
          </div>
  `);
}

/**
 *
 * Adds video on HTML, appends inside video-container.
 */
function addVideoToPage(video) {
  const $video = generateHtmlMarkup(video);
  $(".video-container").append($video);
}


/**
 * Event for clicking Genie lamp -> sends request to backend, calls YouTube
 * API and returns a response. Append video to display on screen.
 *
 * If no video is found (status code 200)--> loop back to request again.
 * If 3rd and final video is displayed, receive 403 --> redirect to Genie page.
 */
async function displayVideo(evt) {
  evt.preventDefault();
  $(".video-container").empty();
  $('#magic-lamp-graphic').attr('src', '/static/images/lamp-3.png');

  let response;
  do {
    response = await fetch(WISH_API_ENDPOINT, {
      method: "POST",
    });
    console.log(response.status, "response status");
    if (response.status === 403) {
      callGenie();
    }
  } while (response.status === 200);

  if (response.status === 201) {
    const videoData = await response.json();
    $('#magic-lamp-graphic').attr('src', '/static/images/lamp-container-3.png');
    addVideoToPage(videoData);
  }
}
//Event for clicking on lamp.
$('#lamp-video-display').on('click', displayVideo);


/**
 * Timeout function that enables locked button in nav--> changes text and color.
 * Allows user to click the link to visit genie, or redirects in approx. 15 sec.
 */
function callGenie() {
  setTimeout(() => {
    window.location.href = '/genie';
  }, 15000);
  const genieReadySnd = document.getElementById('genieReady');
  if (genieReadySnd) {
    genieReadySnd.play();
  }

  $('#magic-lamp-graphic').attr('src', '/static/images/lamp-smoke-3.png');
  $('#magic-lamp-graphic').css({
    'animation': 'flash 2s infinite',
  });
  $("#nav-bar-locked").text("Visit Genie").removeClass("btn-light");
  $("#nav-bar-locked").addClass("activate-genie-button").prop("disabled", false);
}
//
/**
 * Event for favoriting a video. Adds video to user's favorite list, and
 * changes button.
*/
async function favorite(evt) {
  evt.preventDefault();

  const $evtTarget = $(evt.target);
  const $button = $evtTarget.closest('button');
  const videoId = $button.data('id');
  console.log(videoId, "video Id");

  const response = await fetch(`${SEND_FAVORITE}/${videoId}`, {
    method: "POST",
  });
  const favorite = await response.json();
  console.log(await favorite, "favorite response");


  //Change value of button to new image
  $button.toggleClass('unfavorite-button');

  if ($button.hasClass('unfavorite-button')) {
    $button.css({
      'background-color': '',
      'color': 'red'
    }).html('<i id="video-favorite-display" class="bi bi-heart-fill"></i>');
  } else {
    $button.css({
      'background-color': '',
      'color': 'gray'
    }).html('<i id="video-favorite-display" class="bi bi-heart"></i>');
  }
}
//Event for favoriting video.
$('.video-container').on('click', '#favorite-button', favorite);



