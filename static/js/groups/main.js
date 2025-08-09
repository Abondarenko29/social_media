var textarea = document.getElementById("markdownify");
textarea.removeAttribute("required")

function showMenu(article_pk) {
    let menu = document.getElementById("inner-menu" + article_pk)
    if (menu.classList.contains("closed")) {
        menu.classList.remove("closed");
    }
    else {
        menu.classList.add("closed");
    };
}

function toggleReplies(repliedArticlePk, button) {
    var article_list = document.getElementById("article-list" + repliedArticlePk);
    if (button.innerText == "Replies ↷") {
        article_list.classList.remove("closed");
        button.innerText = "Hide ⇡"
    }
    else {
        article_list.classList.add("closed");
        button.innerText = "Replies ↷"
    };
  };
