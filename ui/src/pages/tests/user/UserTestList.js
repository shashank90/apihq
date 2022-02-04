import "./userTestList.css";
import { DataGrid } from "@material-ui/data-grid";
import { useContext } from "react";
import { Link } from "react-router-dom";
import UserTestsContext from "../../../store/usertests-context";

export default function UserTestList() {
  const userTestsCtx = useContext(UserTestsContext);
  const contextData = userTestsCtx.contextData;
  const isLoading = userTestsCtx.isLoading;

  console.log(contextData);

  const data = contextData.getUserTests();

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "name",
      headerName: "Name",
      width: 300,
      renderCell: (params) => {
        return <div className="uTestListItem">{params.row.name}</div>;
      },
    },
    {
      field: "description",
      headerName: "Description",
      width: 400,
      renderCell: (params) => {
        return <div className="uTestListItem">{params.row.description}</div>;
      },
    },
    {
      field: "Enabled",
      headerName: "Enabled",
      width: 200,
      renderCell: (params) => {
        return <div className="uTestListItem">{params.row.enabled}</div>;
      },
    },
    {
      field: "action",
      headerName: "Action",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            <Link
              to={{
                pathname: "/tests/" + params.row.linkName,
              }}
            >
              <button className="msgListView">Edit</button>
            </Link>
          </>
        );
      },
    },
  ];

  return (
    <div className="uTestList">
      <h1>User Tests</h1>
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
