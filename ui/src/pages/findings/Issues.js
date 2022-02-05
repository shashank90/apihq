import "./issues.css";
import styles from "../../components/common/errors.css";
import { DataGrid } from "@material-ui/data-grid";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import IssueDetails from "./IssueDetails.js";

const getIssuesBaseURL = "http://localhost:3000/apis/v1/issues";

export default function Issues(props) {
  const [issueSelected, setIssueSelected] = useState(false);
  const [issueDetail, setIssueDetail] = useState({});
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const params = useParams();
  let specId = params.specId;
  // TODO: Remove hard-coding
  specId = "S0844c74de3ed4768a1c3c833f98daa74";
  console.log(specId);

  function showIssueDetails(id) {
    console.log("Row with id clicked: " + id);
    // console.log(data);
    const issueS = issues.filter((item) => {
      return item.id === id;
    });
    if (issueS) {
      const issue = issueS[0];
      console.log(issue);
      setIssueDetail(issue);
      setIssueSelected(true);
    }
  }

  const fetchIssuesHandler = useCallback(async () => {
    setLoading(true);
    setError(null);
    const getIssuesURL = getIssuesBaseURL + "/" + specId;
    try {
      const response = await fetch(getIssuesURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token":
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZjdhZDIyMTMtMTZiOS00MDE2LThhZGUtYjA3MjNmNDdlOWFkIiwiZXhwIjoxNjQ0NDI0OTU1fQ.YlWL5pP4ZNqMJpDFG9El0m63Drp0jQk1RIcsd39ETDc",
        },
      });
      const data = await response.json();
      console.log(data);
      // Set error and other success message(if any)
      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }

      // Set Issues
      const transformedIssues = data.issues.map((issue, index) => {
        return {
          id: index + 1,
          description: issue.description,
          message: issue.message,
        };
      });
      setIssues(transformedIssues);
    } catch (error) {
      setError(error.message);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchIssuesHandler();
  }, [fetchIssuesHandler]);

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "description",
      headerName: "Description",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.description}</div>;
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

  let content = <div></div>;

  if (issues.length > 0) {
    content = (
      <DataGrid
        rows={issues}
        disableSelectionOnClick
        columns={columns}
        pageSize={8}
        checkboxSelection
      />
    );
  }

  if (error) {
    content = <p className={styles.error_text}>{error}</p>;
  }

  if (issueSelected) {
    return (
      <IssueDetails detail={issueDetail} setIssueSelected={setIssueSelected} />
    );
  } else {
    return (
      <div className="vulnsWrapper">
        <h1>Issues</h1>
        {content}
      </div>
    );
  }
}
