"use strict";

const WISH_API_ENDPOINT = '/wish';
const SEND_FAVORITE = '/favorite_video';
const $box = $('#box');
window.addEventListener('scroll', moveGenie, { passive: true });

/**
 * Event for moving splash page image--> follows mouse.
 */
function moveGenie(evt) {
  const x = evt.clientX / window.innerWidth - 0.5;
  const y = 0.5 - evt.clientY / window.innerHeight;

  const rotationX = y * 180;
  const rotationY = x * 180;

  $box.css('transform', `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`);
};
//Event for moving splash image.
$(document).on('mousemove', moveGenie);


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
          <button class="btn btn-outline-primary btn-sm"
          id="favorite-button"
          data-id="${video.id}"
          type="submit">Favorite</button>
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
      'background-color': 'red',
      'color': 'white'
    }).text('Unfavorite');
  } else {
    $button.css({
      'background-color': '',
      'color': 'blue'
    }).text('Favorite');
  }
}
//Event for favoriting video.
$('.video-container').on('click', '#favorite-button', favorite);
