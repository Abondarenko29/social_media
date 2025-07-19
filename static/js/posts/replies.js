function toggleReplies(repliedCommentPk, button) {
    var comment_list = document.getElementById("comment-list" + repliedCommentPk);
    if (button.innerText == "Replies ↷") {
        comment_list.classList.remove("closed");
        button.innerText = "Hide ⇡"
    }
    else {
        comment_list.classList.add("closed");
        button.innerText = "Replies ↷"
    };
  };

function showForm(pk, button) {
    var comment_form = document.getElementById("comment-form" + pk);
    if (button.innerText == "Answer") {
        comment_form.classList.remove("closed");
        button.classList.add("not-main");
        button.innerText = "Cancel";
        document.getElementById("main-comment-form").classList.add("closed");
    }
    else {
        comment_form.classList.add("closed");
        button.classList.remove("not-main");
        button.innerText = "Answer";
        document.getElementById("main-comment-form").classList.remove("closed");
    }
};

function submitForm(pk) {
    var comment_form = document.getElementById("comment-form" + pk);
    comment_form.classList.add("closed");
    document.getElementById("main-comment-form").classList.remove("closed");
}

function showMenu(comment_pk) {
    var inner_menu = document.getElementById("inner-menu" + comment_pk);
    if (inner_menu.classList.contains("closed")) {
        inner_menu.classList.remove("closed");
    }
    else {
        inner_menu.classList.add("closed");
    };
}
