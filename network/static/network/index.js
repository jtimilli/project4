document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like-button, .unlike-button").forEach(button => {
    button.addEventListener("click", toggleLike);
  });
});

function toggleLike() {
  const postId = this.dataset.postid;
  console.log(postId, "Post Id");
  fetch(`likes/${postId}/`, { method: "POST", body: JSON.stringify({}) })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      const likesCountElement = document.querySelector(
        `.like-button[data-postid="${postId}"] ~ #likes-count`
      );
      likesCountElement.innerText = `${result.likes_count} Likes`;

      const likeButtonElement = document.querySelector(
        `.like-button[data-postid="${postId}"]`
      );
      if (result.liked) {
        likeButtonElement.innerHTML = "unliked";
      } else {
        likeButtonElement.innerHTML = "like";
      }
      likeButtonElement.dataset.liked = result.liked;
    });
}
