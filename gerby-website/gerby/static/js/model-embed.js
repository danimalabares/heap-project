// A link to an interactive model
// (/models/<chapter>/<name>.html) that follows a
// figure puts a play button on that figure. The
// model is loaded in place only on click.
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
    if (!pattern.test(path)) {
      return;
    }
    var image = figureBefore(this);
    if (!image.length || image.parent().is(".model-embed")) {
      return;
    }
    // No button for a model the site does not serve.
    $.ajax({url: path, method: "HEAD"}).done(function() {
      embed(image, path);
    });
  });

  function embed(image, path) {
    if (image.parent().is(".model-embed")) {
      return;
    }
    image.wrap('<span class="model-embed"></span>');
    var holder = image.parent();
    var play = $(
      '<button type="button" class="model-play"' +
      ' aria-label="Play the interactive model"' +
      ' title="Play the interactive model">' +
      "&#9654;</button>"
    );
    var close = $(
      '<button type="button" class="model-close">' +
      "Back to the figure</button>"
    );
    var frame = null;
    holder.append(play);

    function open() {
      frame = $("<iframe>", {
        src: path,
        title: "Interactive model",
        allow: "fullscreen"
      });
      image.hide();
      play.hide();
      holder.addClass("model-open").append(frame, close);
    }

    play.on("click", open);
    image.on("click", open);
    close.on("click", function() {
      frame.remove();
      close.detach();
      holder.removeClass("model-open");
      image.show();
      play.show();
    });
  }
});
