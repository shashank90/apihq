import styles from "./apiRun.module.css";
import React, { useState, useCallback, useEffect, useContext } from "react";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
// import { DataGrid } from "@material-ui/data-grid";
import { Link } from "react-router-dom";
import ReactDOM from "react-dom";
import APIDropdownModal from "../../components/apiSelector/ApiSelectorModal";
import Backdrop from "../../components/common/Backdrop";
import AuthContext from "../../store/auth-context";
import DataTable from "../../components/dataTable/DataTable";

const getRunsURL = "http://localhost:3000/apis/v1/runs";

export default function APIScan() {
  const [runs, setRuns] = useState([]);
  const [dropdownModalIsOpen, setDropdownModalIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const authCtx = useContext(AuthContext);

  function showDropdownHandler() {
    setDropdownModalIsOpen(true);
  }

  function closeDropdownHandler() {
    setDropdownModalIsOpen(false);
  }

  const fetchRunHandler = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(getRunsURL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": authCtx.token,
        },
      });

      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        console.log("Response status: " + response.status);
        if ("error" in data) {
          throw new Error(data.error.message);
        }
        throw new Error(data.message);
      } else {
        const runs = data.runs.map((api, index) => {
          return {
            id: index + 1,
            runId: api.run_id,
            httpMethod: api.http_method,
            endpointURL: api.api_endpoint_url,
            status: api.status,
          };
        });
        setRuns(runs);
      }
    } catch (error) {
      setError(error.message);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchRunHandler();
    // const interval = setInterval(() => {
    //   fetchRunHandler();
    // }, 20000);
    // return () => clearInterval(interval);
  }, [fetchRunHandler]);

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "HTTP Method",
      headerName: "HTTP Method",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.httpMethod}</div>;
      },
    },
    {
      field: "Endpoint URL",
      headerName: "Endpoint URL",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.endpointURL}</div>;
      },
    },
    // {
    //   field: "Last Run",
    //   headerName: "Last Run",
    //   width: 200,
    //   renderCell: (params) => {
    //     return <div className="TargetListItem">{params.row.site}</div>;
    //   },
    // },
    {
      field: "Status",
      headerName: "Status",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.status}</div>;
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
                pathname: `/apis/run/issues/${params.row.runId}`,
              }}
            >
              <button className="msgListView">View</button>
            </Link>
          </>
        );
      },
    },
  ];

  // console.log(dropdownModalIsOpen);

  let content = <DataTable data={runs} columns={columns} />;

  if (error) {
    content = <p>{error}</p>;
  }

  if (loading) {
    content = <p>Loading...</p>;
  }

  if (dropdownModalIsOpen) {
    return (
      <div className="card">
        {ReactDOM.createPortal(
          <Backdrop onCancel={closeDropdownHandler} />,
          document.getElementById("backdrop-root")
        )}
        {ReactDOM.createPortal(
          <APIDropdownModal
            onCancel={closeDropdownHandler}
            onConfirm={closeDropdownHandler}
          />,
          document.getElementById("overlay-root")
        )}
      </div>
    );
  } else {
    return (
      <div className={styles.TargetList}>
        <div className={topbarStyles.new_action_container}>
          <h1 className={styles.TargetTitle}>Run</h1>
          <button
            className={buttons.new_action_btn}
            onClick={() => showDropdownHandler()}
          >
            Run API
          </button>
        </div>
        {content}
      </div>
    );
  }
}
