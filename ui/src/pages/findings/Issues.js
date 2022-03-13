import "./issues.css";
import styles from "../../components/common/errors.css";
import buttons from "../../components/common/buttons.module.css";
import { useState, useCallback, useEffect, useContext } from "react";
import { DataGrid } from "@material-ui/data-grid";
import { useParams } from "react-router-dom";
import IssueDetails from "./IssueDetails.js";
import AuthContext from "../../store/auth-context";

const getIssuesBaseURL = "/apis/v1/issues";

export default function Issues(props) {
  const [issueSelected, setIssueSelected] = useState(false);
  const [issueDetail, setIssueDetail] = useState({});
  const [issues, setIssues] = useState([]);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const authCtx = useContext(AuthContext);

  const params = useParams();
  let runId = params.runId;

  function showIssueDetails(id) {
    // console.log(data);
    // Find issue by id and corresponding request
    const issueS = issues.filter((item) => {
      return item.id === id;
    });
    if (issueS) {
      const issue = issueS[0];
      // console.log(issue);
      const requestId = issue.requestId;
      // console.log("requestId: " + requestId);

      // Set corresponding request
      const requestS = requests.filter((request) => {
        return request.request_id === requestId;
      });

      let requestSelected = null;
      if (requestS) {
        requestSelected = requestS[0];
        // console.log(request);
      }
      setIssueDetail({ issue: issue, request: requestSelected });
      setIssueSelected(true);
    }
  }

  const fetchIssuesHandler = useCallback(async () => {
    setLoading(true);
    setError(null);
    const getIssuesURL = getIssuesBaseURL + "/" + runId;
    try {
      const response = await fetch(getIssuesURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });
      const data = await response.json();
      // console.log(data);
      // Set error and other success message(if any)
      if (!response.ok) {
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      }

      // Set Issues
      const transformedIssues = data.issues.map((issue, index) => {
        return {
          id: index + 1,
          requestId: issue.request_id,
          issueType: issue.issue_type,
          message: issue.message,
          description: issue.description,
          solution: issue.solution,
        };
      });
      setIssues(transformedIssues);
      setRequests(data.requests);
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
      field: "Type",
      headerName: "Type",
      width: 400,
      renderCell: (params) => {
        return <div className="msgListItem">{params.row.issueType}</div>;
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
              className={buttons.green_btn}
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
      <IssueDetails
        issueDetail={issueDetail}
        setIssueSelected={setIssueSelected}
      />
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
