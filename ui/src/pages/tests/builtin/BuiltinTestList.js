import "./builtinTestList.css";
import { DataGrid } from "@material-ui/data-grid";
import { useContext } from "react";
import { Link } from "react-router-dom";
import BuiltinTestsContext from "../../../store/builtintests-context";

export default function BuiltinTestList() {
  const builtinTestsCtx = useContext(BuiltinTestsContext);
  const contextData = builtinTestsCtx.contextData;
  const isLoading = builtinTestsCtx.isLoading;

  console.log(contextData);

  const data = contextData.getBuiltinTests();

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "name",
      headerName: "Name",
      width: 400,
      renderCell: (params) => {
        return <div className="bTestListItem">{params.row.name}</div>;
      },
    },
    {
      field: "CWE ID",
      headerName: "CWE ID",
      width: 200,
      renderCell: (params) => {
        return <div className="bTestListItem">{params.row.cweId}</div>;
      },
    },
    {
      field: "WASC ID",
      headerName: "WASC ID",
      width: 200,
      renderCell: (params) => {
        return <div className="bTestListItem">{params.row.wascId}</div>;
      },
    },
    {
      field: "Enabled",
      headerName: "Enabled",
      width: 200,
      renderCell: (params) => {
        return <div className="bTestListItem">{params.row.enabled}</div>;
      },
    },
  ];

  return (
    <div className="bTestList">
      <h1>Built-in Tests</h1>
      <DataGrid
        rows={data}
        disableSelectionOnClick
        columns={columns}
        pageSize={8}
        checkboxSelection
      />
    </div>
  );
}
