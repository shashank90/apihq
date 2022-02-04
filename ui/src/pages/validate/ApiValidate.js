import "./apiValidate.css";
import { DataGrid } from "@material-ui/data-grid";
import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import { targetList } from "../../store/dummyData";

export default function ApiValidate() {
  const [data, setData] = useState(targetList);
  const location = useLocation();

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "Spec Id",
      headerName: "Spec Id",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Collection name",
      headerName: "Collection name",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Status",
      headerName: "Status",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Message",
      headerName: "Message",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Result",
      headerName: "Result",
      width: 200,
      renderCell: (params) => {
        return (
          <>
            <Link
              to={{
                pathname: `/apis/spec/editor/${params.row.id}`,
                state: { prevPath: location.pathname },
              }}
            >
              <button className="msgListView">Validate</button>
            </Link>
          </>
        );
      },
    },
  ];

  return (
    <div className="TargetList">
      <div className="TargetTitleContainer">
        <h1 className="TargetTitle">Validate</h1>
      </div>
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
