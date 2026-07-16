$(document).ready(function() {
  var environments = [
    "definition",
    "example",
    "exercise",
    "lemma",
    "proposition",
    "remark",
    "remarks",
    "situation",
    "theorem"
  ];
  var selector = environments.map(
    function(environment) {
      return "article.env-" + environment;
    }
  ).join(",");

  $(selector).each(function(index, element) {
    var article = $(element);
    var tagged = article.find("[data-tag]")
      .first();
    var tag = tagged.attr("data-tag")
      || article.attr("id");

    if (!/^[0-9A-Z]{4}$/.test(tag)) {
      return;
    }

    var href = "/tag/" + tag;
    var identifier = article.find(
      ".environment-identifier"
    ).first();

    if (identifier.length) {
      if (identifier.is("a")) {
        identifier.attr("href", href);
        identifier.attr("data-tag", tag);
      } else {
        identifier.wrap(
          $("<a>", {
            "class":
              "environment-identifier",
            "data-tag": tag,
            "href": href
          })
        );
        identifier.removeClass(
          "environment-identifier"
        );
      }
    }

    article.attr(
      "data-environment-href",
      href
    );
  });

  $(selector).on("click", function(event) {
    var target = $(event.target);

    if (target.closest(
      "a, button, input, textarea, select"
    ).length) {
      return;
    }

    var selection = window.getSelection();
    if (selection && selection.toString()) {
      return;
    }

    var href = $(this).attr(
      "data-environment-href"
    );

    if (href) {
      window.location.assign(href);
    }
  });
});
