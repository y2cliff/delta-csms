const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable, {
      perPageSelect: [10, 25, 50, ["All", -1]],
      columns: [{
          select: 2,
          sortSequence: ["desc", "asc"]
        },
        {
          select: 3,
          sortSequence: ["desc"]
        },
        {
          select: 4,
          cellClass: "green",
          headerClass: "red"
        }
      ]
    });
  })
