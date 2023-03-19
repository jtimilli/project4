document.addEventListener("DOMContentLoaded", () => {
  const likeButtons = document.querySelectorAll(".like-button");
  likeButtons.forEach(button => {
    button.addEventListener("click", function () {
      const postId = this.dataset.postid;
      toggleLike(postId);
    });
  });
});

function toggleLike(postId) {
  fetch(`likes/${postId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      const likesCountElement = document.querySelector(
        `.like-button[data-postid="${postId}"] ~ #likes-count`
      );
      //returns liek
      likesCountElement.innerText = `${result.likes_count} likes`;
      const likeButtonElement = document.querySelector(
        `.like-button[data-postid="${postId}"]`
      );
      if (result.liked) {
        likeButtonElement.innerHTML = `Unlike`;
      } else {
        likeButtonElement.innerHTML = `Like`;
      }
    });
}
