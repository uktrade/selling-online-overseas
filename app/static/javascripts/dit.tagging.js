// SOO Specific Tagging Functionality.
// -----------------------------------
// REQUIRES
// jQuery
// dit.js


// Because we're not on ExOpps, which has the full set
// of files, adding a little defensive namespacing.
var dit = dit || {};
dit.tagging = dit.tagging || {};


// Event tagging for SOO page types.
dit.tagging.soo = (new function() {

  this.init = function(page) {
    $(document).ready(function() {

      // All pages
      addTaggingForFeedbackForm();

      // Individual pages
      switch(page) {
        case 'LandingPage':
          addTaggingForStories();
          addTaggingForSearch();
        break;

        case 'SearchResultsPage':
          addTaggingForSearch();
        break;

        case 'MarketplacePage':
          addTaggingForApply();
          addTaggingForMarketLink();
        break;

        default: // nothing
      }
    });
  }

  function addTaggingForStories() {
    $("#exporter-stories a").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'ExporterStory',
        'element': 'Link',
        'value': $(this).find("h3").text()
      });
    });
  }

  function addTaggingForSearch() {
    $("#results-form").on("submit", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Search',
        'type': 'Marketplace',
        'element': 'SearchForm',
        'value': $(this).find("[name='category_id']").val() + "|" + $(this).find("[name='country_id']").val()
      });
    });
  }

  function addTaggingForApply() {
    $("#apply-to-join").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'MarketApplication',
        'element': 'Link',
        'value': $(this).attr("href").replace(/.*\?market=([\w\s]+)/, "$1")
      });
    });
    $("#bottom-apply-to-join").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'MarketApplication',
        'element': 'Link',
        'value': $(this).attr("href").replace(/.*\?market=([\w\s]+)/, "$1")
      });
    });
  }

  function addTaggingForMarketLink() {
    $(".markets-group .link").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'ContentLink',
        'type': 'Marketplace',
        'element': 'MarketDetailsLink',
        'value': $(this).text()
      });
    });
  }


  function addTaggingForFeedbackForm() {
    $(".thumber-form button").on("click", function() {
      window.dataLayer.push({
        'event': 'gaEvent',
        'action': 'Cta',
        'type': 'Feedback',
        'element': 'ThumberButton',
        'value': $(this).text()
      });
    });
  }
});
