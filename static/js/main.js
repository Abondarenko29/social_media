function togglePanel(container, panel, collapse) {
    if (typeof collapse === 'undefined') {
      collapse = panel.getAttribute('aria-hidden') !== 'false';
    }
    if (panel && container) {
      if (collapse) {
        panel.setAttribute('aria-hidden', 'true');
        container.setAttribute('aria-expanded', 'false');
      } else {
        panel.setAttribute('aria-hidden', 'false');
        container.setAttribute('aria-expanded', 'true');
      }
    }
  }
  
  // Add click handler for clicks on elements with aria-controls
  [].slice.call(document.querySelectorAll('.p-search-and-filter')).forEach(function(pattern) {
    var input = pattern.querySelector('.p-search-and-filter__input');
    var container = pattern.querySelector('.p-search-and-filter__search-container');
    input.addEventListener('blur', function(event) {
      var targetPanel = pattern.querySelector('.p-search-and-filter__panel');
      togglePanel(container, targetPanel, true);
    });
    input.addEventListener('focus', function(event) {
      var targetPanel = pattern.querySelector('.p-search-and-filter__panel');
      togglePanel(container, targetPanel, false);
    });
  });


document.getElementById("close-sidebar").addEventListener("click", function() {
  document.getElementById("sidebar").classList.remove("sidebar-opened")
  document.getElementById("sidebar").classList.add("sidebar-closed")
});

document.getElementById("open-sidebar").addEventListener("click", function() {
  document.getElementById("sidebar").classList.remove("sidebar-closed")
  document.getElementById("sidebar").classList.add("sidebar-opened")
});


function wrapText(before, after) {
  const textarea = document.getElementById('markdownify');
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selected = textarea.value.substring(start, end);
  const replacement = before + selected + after;

  textarea.setRangeText(replacement, start, end, 'end');
  textarea.focus();
}

const simplemde = new SimpleMDE({
  element: document.getElementById("markdownify"),
  spellChecker: false,
  status: false,
  toolbar: [
    "bold", "italic", "heading", "|",
    "unordered-list", "ordered-list", "|",
    "link", "quote", "code", "|",
    "image", "preview", "guide", 
  ],
});
