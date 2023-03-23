document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like-button, .unlike-button").forEach(button => {
    button.addEventListener("click", toggleLike);
  });

  document.querySelectorAll(".edit-button").forEach(button => {
    button.addEventListener("click", editPost);
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

function editPost() {
  const postId = this.dataset.postid;

  // Get content of current post
  const content_area = document.querySelector(
    `.content-text[data-postid="${postId}"]`
  );

  const content = content_area.innerText;

  //
  content_area.innerHTML = `<div class="m-3">
    <textarea class="new-content form-control" data-postid="${postId}" name="w3review" rows="4" cols="50">${content}</textarea>
    <br>
    <button class="btn btn-primary btn-sm" role="button" value="Save"> Save </button>
  </div>`;

  // Add event listener to the button
  const saveButton = content_area.querySelector("button");
  saveButton.addEventListener("click", () => {
    const content = document.querySelector(
      `.new-content[data-postid="${postId}"]`
    ).value;

    fetch(`savepost/${postId}/`, {
      method: "PUT",
      body: JSON.stringify({
        content: content,
      }),
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);

        content_area.innerHTML = `<p class="card-text content-text" data-postid="{{ post.id }}">
        ${content}
      </p>`;
      });
  });
}
