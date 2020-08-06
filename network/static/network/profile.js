document.addEventListener("DOMContentLoaded", function() {
    follow_button = document.querySelector("#follow-button");
    follow_button.onclick = () => {
        if (follow_button.innerHTML === "Follow") {
            follow_button.innerHTML = "Following";
        } else {
            follow_button.innerHTML = "Follow";
        }
    };
});
