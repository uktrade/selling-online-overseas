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
    $(".more-stories a").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'ExporterStory',
        'eventLabel': 'Link',
        'eventValue': $(this).find("h3").text()
      });
    });
  }

  function addTaggingForSearch() {
    $("#results-form").on("submit", function() {
      window.dataLayer.push({
        'eventAction': 'Search',
        'eventCategory': 'Marketplace',
        'eventLabel': 'SearchForm',
        'eventValue': $(this).find("#search-product").val() + "|" + $(this).find("#search-country").val()
      });
    });

    // Only applicable to Home page.
    $("button:contains('Start your search now')[data-scrollto]").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'Search',
        'eventLabel': 'Link',
        'eventValue': $(this).text()
      });
    });
  }

  function addTaggingForApply() {
    $("#apply-to-join").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'MarketApplication',
        'eventLabel': 'Link',
        'eventValue': $(this).attr("href").replace(/.*\?market=([\w\s]+)/, "$1")
      });
    });
    $("#bottom-apply-to-join").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'MarketApplication',
        'eventLabel': 'Link',
        'eventValue': $(this).attr("href").replace(/.*\?market=([\w\s]+)/, "$1")
      });
    });
  }

  function addTaggingForMarketLink() {
    $(".markets-group .link").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'ContentLink',
        'eventCategory': 'Marketplace',
        'eventLabel': 'MarketDetailsLink',
        'eventValue': $(this).text()
      });
    });
  }


  function addTaggingForFeedbackForm() {
    $(".thumber-form button").on("click", function() {
      window.dataLayer.push({
        'eventAction': 'Cta',
        'eventCategory': 'Feedback',
        'eventLabel': 'ThumberButton',
        'eventValue': $(this).text()
      });
    });
  }
});
