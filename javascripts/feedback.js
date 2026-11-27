/* Page feedback shim.
 *
 * Material's built-in feedback widget (partials/feedback.html) is only
 * wired up by the analytics provider JS: the provider script unhides
 * the form and reveals the note when a rating is clicked. With no
 * analytics provider configured yet, this shim does exactly that job —
 * the same behaviour Material's own handler provides — so the widget
 * works with no backend at all. The note on each rating links to a
 * pre-filled GitHub Discussion, which is where the feedback lands.
 *
 * Once a Google Analytics property is configured (extra.analytics in
 * mkdocs.yml), __md_analytics exists and this shim does nothing:
 * Material's own handler takes over (and also sends the vote to GA).
 */
(function () {
  if (typeof __md_analytics !== "undefined") return;
  var form = document.forms.feedback;
  if (!form) return;
  form.hidden = false;
  var buttons = form.querySelectorAll("[type=submit]");
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function (event) {
      event.preventDefault();
      var value = this.getAttribute("data-md-value");
      var note = form.querySelector(
        '.md-feedback__note [data-md-value="' + value + '"]'
      );
      if (note) note.hidden = false;
      form.firstElementChild.disabled = true;
    });
  }
})();
