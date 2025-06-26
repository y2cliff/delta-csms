$(document).ready(function() {
    $("#btnFetch").click(function() {
      // load data via AJAX
      fetch_data($("#inputTopic").val());
      // disable button
      $(this).prop("disabled", true);
      // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading...`
      );
    });
});