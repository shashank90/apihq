import styles from "./apiRun.module.css";
import React, { useState, useEffect, useContext } from "react";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
// import { DataGrid } from "@material-ui/data-grid";
import { Link } from "react-router-dom";
import ReactDOM from "react-dom";
import APIDropdownModal from "../../components/apiSelector/ApiSelectorModal";
import Backdrop from "../../components/common/Backdrop";
import AuthContext from "../../store/auth-context";
import DataTable from "../../components/dataTable/DataTable";
import { DATA_REFRESH_FREQUENCY } from "../../store/constants";

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

  function updateRuns(fetchedRuns) {
    if (runs.length > 0) {
      if (JSON.stringify(runs) === JSON.stringify(fetchedRuns)) {
        console.log("Matched!!. No change");
      } else {
        console.log("Change DETECTED..");
        setRuns(fetchedRuns);
      }
    } else {
      setRuns(fetchedRuns);
    }
  }
  async function fetchApiRunDataFirstTime() {
    setLoading(true);
    setError(null);
    fetchApiRunDataPeriodic();
    setLoading(false);
  }

  async function fetchApiRunDataPeriodic() {
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
        const fetchedRuns = data.runs.map((api, index) => {
          return {
            id: index + 1,
            runId: api.run_id,
            endpointURL: api.api_endpoint_url,
            httpMethod: api.http_method,
            updated: api.updated,
            status: api.status,
          };
        });
        updateRuns(fetchedRuns);
      }
    } catch (error) {
      setError(error.message);
    }
  }

  useEffect(() => {
    console.log("Fetch Api Run data on first load...");
    fetchApiRunDataFirstTime();
    const interval = setInterval(() => {
      fetchApiRunDataPeriodic();
    }, DATA_REFRESH_FREQUENCY);
    return () => clearInterval(interval);
  }, []);

  // console.log(dropdownModalIsOpen);

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "Run Id",
      headerName: "Run Id",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.runId}</div>;
      },
    },
    {
      field: "Endpoint URL",
      headerName: "Endpoint URL",
      width: 350,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.endpointURL}</div>;
      },
    },
    {
      field: "HTTP Method",
      headerName: "HTTP Method",
      width: 170,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.httpMethod}</div>;
      },
    },
    {
      field: "Status",
      headerName: "Status",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.status}</div>;
      },
    },
    {
      field: "Updated",
      headerName: "Updated",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.updated}</div>;
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
              <button className={buttons.green_btn}>View</button>
            </Link>
          </>
        );
      },
    },
  ];

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
