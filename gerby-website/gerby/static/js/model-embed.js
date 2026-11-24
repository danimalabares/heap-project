// A link to an interactive model
// (/models/<chapter>/<name>.html) that follows a
// figure replaces that figure by the live model.
// The figure stays in the PDF, and on the site
// when the model is not served.
$(document).ready(function() {
  var pattern = /\/models\/[a-z0-9-]+\/[a-z0-9-]+\.html$/;

  function figureBefore(link) {
    var block = $(link).closest("p");
    var previous = block.prev();
    for (var i = 0; i < 4 && previous.length; i++) {
      var image = previous.is("img")
        ? previous : previous.find("img").last();
      if (image.length) {
        return image;
      }
      previous = previous.prev();
    }
    return $();
  }

  $("#tag a[href*='/models/']").each(function() {
    var path = this.pathname;
    var step = this.search + this.hash;
    if (!pattern.test(path)) {
      return;
    }
    var image = figureBefore(this);
    if (!image.length) {
      return;
    }
    $.ajax({url: path, method: "HEAD"}).done(function() {
      if (!image.parent().length) {
        return;
      }
      var frame = $("<iframe>", {
        "class": "model-embed",
        // Sized here too: a browser may hold an
        // older stylesheet for hours.
        style: "display:block;width:100%;max-width:700px;" +
          "height:840px;margin:1.6em auto;border:1px solid #d8d8d8;" +
          "border-radius:6px;background:#fff",
        src: path + step,
        title: "Interactive model",
        loading: "lazy",
        allow: "fullscreen"
      });
      // The model takes the place of the whole
      // figure, also when it has several pictures.
      var figure = image.parent();
      if (figure.is("div.centered, figure")) {
        figure.empty().append(frame);
      } else {
        image.replaceWith(frame);
      }
    });
  });
});
