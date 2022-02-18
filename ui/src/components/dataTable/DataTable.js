import { DataGrid } from "@material-ui/data-grid";
import React from "react";

function DataTable(props) {
  console.log("Inside data table");
  return (
    <DataGrid
      rows={props.data}
      disableSelectionOnClick
      columns={props.columns}
      pageSize={8}
      checkboxSelection
    />
  );
}

export default React.memo(DataTable);
