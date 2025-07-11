<script>

  let workHrsPerActCtx = document.getElementById("workHrsPerActChart").getContext("2d");
  let barChart = new Chart(workHrsPerActCtx, {
    type: "bar",
    options: {
      responsive: true,
      interaction: {
        intersect: false,
      },
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      },
      title: {
        display: false,
        text: ""
      }
    }
  });
</script>

<script>
  const contextDiv = document.getElementById("contextDiv");
  const card_no = contextDiv.dataset.card_no;
  // console.log(contextDiv.dataset);  

  $(document).ready(function() {
    $.ajax({
      url: "/pledge/chart/filter-options/",
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {

        // Load all the options
        jsonResponse.options.forEach(option => {
          $("#year").append(new Option(option, option));
        });

        // Load data for the first option
        loadAllCharts(card_no,  $("#year").children().first().val());

      },
      error: () => console.log("Failed to fetch chart filter options!")
    });
  });

  $("#filterForm").on("submit", (event) => {
    event.preventDefault();
    const year = $("#year").val();
    // const card_no = jsonResponse.card_no;
    loadAllCharts(card_no, year)
  });

  function loadChart(chart, endpoint) {
    $.ajax({
      url: endpoint,
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {
        // Extract data from the response
        const title = jsonResponse.title;
        const labels = jsonResponse.data.labels;
        const datasets = jsonResponse.data.datasets;

        // Reset the current chart
        chart.data.datasets = [];
        chart.data.labels = [];

        // Load new data into the chart
        chart.options.title.text = title;
        chart.options.title.display = true;
        chart.data.labels = labels;
        datasets.forEach(dataset => {
          chart.data.datasets.push(dataset);
        });
        chart.update();
      },
      error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
  }

  function loadAllCharts(card_no, year) {
    loadChart(barChart, `/pledge/card-contrib-per-month/${card_no}/${year}/`);
  }
</script>