let API_KEY = "AIzaSyBYFIsOzpJLb_MS2yh1Ns1gD4WkopMFWuY";

let usernames = [
  "hormel health labss",
  "Climate Change Is Real",
  "Ram Abdullah",
  "ayaz abdullah",
  "Mahesh Kumar Rajesh",
];

var invocation = new XMLHttpRequest();

async function processText(str) {}

function isFalse(rating) {
  return (
    rating.length > 10 ||
    rating.includes("false") ||
    rating.includes("fake") ||
    rating.includes("incorrect") ||
    rating.includes("wrong") ||
    rating.includes("misleading")
  );
}

function linkText(text, link) {
  return (
    '<div><a style="text-decoration: none; color: white;" rel="noopener noreferrer" target="_blank" href="' +
    link +
    '">' +
    text +
    "</a></div>"
  );
}

function removeAlert(text) {
  return "<div><button class='alertButton'>" + text + "</button></div>";
}

function alertTextContent(text, link) {
  return (
    removeAlert("View post") +
    "<div style='color: white; font:inherit; font-size: 20px;'>" +
    text +
    "</div>" +
    linkText("Know more", link)
  );
}

function addAlert(tweet, link) {
  tweet.style.opacity = "0.25";
  var alert = document.createElement("div");
  alert.setAttribute(
    "style",
    "padding: 1vh 1vw 1vh 1vw; border-radius: 10px; border: 1px solid white; margin: 0 1vw 0.5vh 1vw;"
  );

  var alertText = document.createElement("div");
  alertText.setAttribute(
    "style",
    "display: flex; justify-content: space-between;"
  );
  alertText.innerHTML = alertTextContent(
    "This content may be misleading",
    link
  );

  alert.appendChild(alertText);
  tweet.parentNode.appendChild(alert);
  console.log(alertText.childNodes.item(0));
  alertText.childNodes
    .item(0)
    .childNodes.item(0)
    .addEventListener("click", (event) => {
      tweet.style.opacity = "1";
      alert.remove();
    });
}

function reqListener(event) {
  const tweets = event.target.tweetArr;
  const i = event.target.index;
  const tweet = tweets.item(i);
  response = JSON.parse(this.responseText);
  if (!response.claims) {
    return;
  }
  if (tweet.parentNode.parentNode.querySelector("rect") == null) {
    let review = response?.claims[0]?.claimReview[0];
    var link = review?.url;
    var rating = review?.textualRating?.toLowerCase();
    console.log(rating);
    if (isFalse(rating)) {
      addAlert(tweet, link);
    }
  }
}

function cbCheck(event) {
  console.log("Check CB");
  var tweets = event.target.tweetArr;
  var i = event.target.index;
  response = JSON.parse(this.responseText);
  console.log(response.truth);
  var rating = response.truth.toLowerCase();
  if (
    tweets.item(i).parentNode.parentNode.querySelector("rect") == null &&
    (rating.includes("false") ||
      rating.includes("fake") ||
      rating.includes("incorrect") ||
      rating.includes("wrong") ||
      rating.includes("misleading"))
  ) {
    var link = response.url;
    if (link == "undefined") link = null;
    var rating = response.truth.toLowerCase();
    //console.log(rating);
    var username = tweets
      .item(i)
      .parentNode.parentNode.querySelectorAll('[role="link"]')
      .item(1)
      .childNodes.item(0)
      .childNodes.item(0).textContent;
    if (
      rating.length > 10 ||
      rating.includes("false") ||
      rating.includes("fake") ||
      rating.includes("incorrect") ||
      rating.includes("wrong")
    ) {
      var square = document.createElement("div");
      square.innerHTML = htmlBox(
        ele,
        tweets.item(i).parentNode.getBoundingClientRect().bottom -
          tweets.item(i).parentNode.getBoundingClientRect().top +
          20,
        link
      );
      tweets.item(i).parentNode.appendChild(square);
      square.childNodes
        .item(0)
        .childNodes.item(0)
        .childNodes.item(3)
        .addEventListener("click", (event) => {
          event.target.parentNode.parentNode.childNodes.item(0).remove();
        });
      ele++;
    }
  }
}

async function findTweets(API_KEY) {
  var tweets = document.querySelectorAll('[data-testid="tweet"]');
  for (var i = 0; i < tweets.length; i++) {
    var tweet = tweets.item(i);
    var postContainer = tweet.querySelector("[lang]");
    if (postContainer != null) {
      var str = postContainer.textContent;
      console.log(str);
      //   str = await processText(str)
      var username = tweet.parentNode.parentNode
        .querySelectorAll('[role="link"]')
        .item(1)
        .childNodes.item(0)
        .childNodes.item(0).textContent;
      if (usernames.includes(username)) {
        var request = new XMLHttpRequest();
        request.addEventListener("load", reqListener);
        request.tweetArr = tweets;
        request.index = i;
        request.open(
          "GET",
          "https://factchecktools.googleapis.com/v1alpha1/claims:search?" +
            new URLSearchParams({
              languageCode: "en",
              maxAgeDays: 256,
              offset: 0,
              pageSize: 25,
              query: str,
              key: API_KEY,
            })
        );
        request.send();
      } else {
        var request = new XMLHttpRequest();
        var url =
          "https://27cc-106-193-137-8.in.ngrok.io/checktool?claim1=" +
          encodeURIComponent(str);
        request.tweetArr = tweets;
        request.index = i;
        request.addEventListener("load", cbCheck);
        request.open("GET", url, true);
        request.send();
      }
    }
  }
}

findTweets(API_KEY);

document.addEventListener("scroll", throttle(findTweets, 500));

function throttle(fn, wait) {
  var time = Date.now();
  return function () {
    if (time + wait - Date.now() < 0) {
      fn();
      time = Date.now();
    }
  };
}
