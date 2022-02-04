import "./issues.css";
import { DataGrid } from "@material-ui/data-grid";
import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import VulnsContext from "../../store/vulns-context";
import IssueDetails from "./IssueDetails";

export default function Issues(props) {
  const [issueSelected, setIssueSelected] = useState(false);
  const [vulnObject, setVulnObject] = useState({});
  const [vulns, setVulns] = useState([]);
  const params = useParams();
  console.log(params.specId);

  const vulnsCtx = useContext(VulnsContext);
  const contextData = vulnsCtx.contextData;
  const isLoading = vulnsCtx.isLoading;

  const data = contextData.getVulns();
  //setVulns(data);

  function showIssueDetails(id) {
    console.log("Row with id clicked: " + id);
    console.log(data);
    const vulnObjs = data.filter((item) => {
      return item.id === id;
    });
    if (vulnObjs) {
      const vulnObj = vulnObjs[0];
      setVulnObject(vulnObj);
      setIssueSelected(true);
    }
  }

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "alert",
      headerName: "Alert",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.alert}</div>;
      },
    },
    {
      field: "CWE ID",
      headerName: "CWE ID",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.cweid}</div>;
      },
    },
    {
      field: "Confidence",
      headerName: "Confidence",
      width: 200,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.confidence}</div>;
      },
    },
    {
      field: "action",
      headerName: "Action",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            <button
              className="msgListView"
              onClick={() => {
                showIssueDetails(params.row.id);
              }}
            >
              View
            </button>
          </>
        );
      },
    },
  ];

  if (issueSelected) {
    return (
      <IssueDetails
        vulnObject={vulnObject}
        setIssueSelected={setIssueSelected}
      />
    );
  } else {
    return (
      <div className="vulnsWrapper">
        <h1>Issues</h1>
        <DataGrid
          rows={data}
          id={(row) => row.alertRef}
          disableSelectionOnClick
          columns={columns}
          pageSize={8}
          checkboxSelection
        />
      </div>
    );
  }
}
