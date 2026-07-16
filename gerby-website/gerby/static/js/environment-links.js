$(document).ready(function() {
  $("article[id] .environment-identifier")
    .each(function(index, element) {
      var identifier = $(element);
      var article = identifier.closest(
        "article[id]"
      );
      var tag = article.attr("id");

      if (!/^[0-9A-Z]{4}$/.test(tag)) {
        return;
      }

      var href = "/tag/" + tag;

      if (identifier.is("a")) {
        identifier.attr("href", href);
        identifier.attr("data-tag", tag);
        return;
      }

      identifier.wrap(
        $("<a>", {
          "class": "environment-identifier",
          "data-tag": tag,
          "href": href
        })
      );
      identifier.removeClass(
        "environment-identifier"
      );
    });
});
