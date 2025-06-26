<script nonce="csms_custom_script">
        document.addEventListener("DOMContentLoaded", () => {
          var budgetChart = echarts.init(document.querySelector("#budgetChart")).setOption({
            legend: { data: ['Basic', 'Advanced', 'Expert'] },
            radar: {
              // shape: 'circle',
              indicator: [
                { name: 'TECH', max: 50 },
                { name: 'ADM',  max: 50 },
                { name: 'NET',  max: 50 },
                { name: 'SYS',  max: 50 },
                { name: 'SEC',  max: 50 },
                { name: 'COM',  max: 50 }
              ]
            },
            series: [{
              name: 'Budget vs spending',
              type: 'radar',
              data: [
                { value: [32, 24, 26, 18, 24, 24], name: 'Basic' },
                { value: [10, 0, 4, 8, 8, 4], name: 'Advanced' },
                { value: [2, 0, 3, 2, 4, 2], name: 'Expert' }
              ]
            }]
          });
        });
      </script>