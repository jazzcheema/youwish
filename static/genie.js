"use strict";

const WISH_API_ENDPOINT = '/wish';
const SEND_FAVORITE = '/favorite_video';
const $box = $('#box');
const $box2 = $('#box2');
const $box3 = $('#box3');

window.addEventListener('scroll', moveGenie, { passive: true });


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
//Event for moving splash image.
$(document).on('mousemove', moveGenie);


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
//Event for moving login image.
$(document).on('mousemove', moveGenie2);



/**
 * Event for moving Login page Genie Head image--> follows mouse.
 */
function moveLamp(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = -y * 100;
  const rotationY = -x * 100;

  $box3.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);

};
//Event for moving login image.
$(document).on('mousemove', moveLamp);




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
$("#login-button-on-splash").on('click', homepageOk);


//Genie Face Sound

function thwompSound() {
  const genieYellSound = document.getElementById('thwompSnd');
  if (genieYellSound) {
    genieYellSound.play();
  }
}

$('#box2').on('click', thwompSound);

//Login Page Sound Ok
function loginSound() {
  const loginSndOk = document.getElementById('okSoundLogin');
  if (loginSndOk) {
    loginSndOk.play();
  }
}
$("#login-button-page").on('click', loginSound);



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
$("#forgot-button-page").on('click', forgotSound);



//Forgot Password Send Sound
function forgotSendSound() {
  const sendForgotSnd = document.getElementById('forgotPasswordSendSnd');
  if (sendForgotSnd) {
    sendForgotSnd.play();
  }
}
$("#forgot-password-button").on('click', forgotSendSound);



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
$('#signup-button-on-splash').on('click', signupSndSplash);



//Signup Page Sound
function signupSnd() {
  const signupSndSubmit = document.getElementById('signupPageSnd');
  if (signupSndSubmit) {
    signupSndSubmit.play();
  }
}
$('#signup-button').on('click', signupSnd);



//Magic Lamp Wish Sound
function magicLampSnd() {
  const lampWishSnd = document.getElementById('genieLampSnd');
  if (lampWishSnd) {
    lampWishSnd.play();
  }
}
$('#magic-lamp-graphic').on('click', magicLampSnd);


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
$('#nav-bar-home').on('click', homeButtonSound);



//Edit Profile Sound
function editProfileSound() {
  const editSnd = document.getElementById('editProfileSnd');
  if (editSnd) {
    editSnd.play();
  }
}
$('#edit-user-button').on('click', editProfileSound);




//Genie Page Music
window.addEventListener('load', function () {
  const genieSnd = document.getElementById('geniePageSnd');
  if (genieSnd) {
    genieSnd.play();
  }
});



///////////////////////////////////////////////////////////////////////////////
/**
 * Creates HTML for each Video display. This is wrapped inside a 'form' with
 * hidden_tag() already rendered on the page.
 */
function generateHtmlMarkup(video) {
  return $(`
    <ul>
      <p><strong>Views:</strong> ${video.views}</p>
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/${video.id}?controls=0&showinfo=0&modestbranding=1"
        frameborder="0" allowfullscreen>
        </iframe>
          <button
          id="favorite-button"
          data-id="${video.id}"
          type="submit"><i class="bi bi-heart"></i></button>
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
  $("#nav-bar-locked").text("Visit Genie").removeClass("btn-light");
  $("#nav-bar-locked").addClass("activate-genie-button").prop("disabled", false);
}

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
    }).html('<i class="bi bi-heart-fill"></i>');
  } else {
    $button.css({
      'background-color': '',
      'color': 'gray'
    }).html('<i class="bi bi-heart"></i>');
  }
}
//Event for favoriting video.
$('.video-container').on('click', '#favorite-button', favorite);



