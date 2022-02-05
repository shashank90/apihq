import styles from "./apiRun.module.css";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
import { DataGrid } from "@material-ui/data-grid";
import { Link } from "react-router-dom";
import { useState } from "react";
import ReactDOM from "react-dom";
import { targetList } from "../../store/dummyData";
import APIDropdownModal from "../../components/apiSelector/ApiSelectorModal";
import Backdrop from "../../components/common/Backdrop";

export default function APIScan() {
  const [data, setData] = useState(targetList);
  const [dropdownModalIsOpen, setDropdownModalIsOpen] = useState(false);
  const [apiPath, setApiPath] = useState();
  const [authHeaders, setAuthHeaders] = useState();

  function showDropdownHandler() {
    setDropdownModalIsOpen(true);
  }

  function closeDropdownHandler() {
    setDropdownModalIsOpen(false);
  }

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "Endpoint URL",
      headerName: "Endpoint URL",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Last Run",
      headerName: "Last Run",
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
                pathname: `/apis/run/issues/${params.row.id}`,
              }}
            >
              <button className="msgListView">View</button>
            </Link>
          </>
        );
      },
    },
  ];

  console.log(dropdownModalIsOpen);

  if (dropdownModalIsOpen) {
    return (
      <div className="card">
        {ReactDOM.createPortal(
          <Backdrop onCancel={closeDropdownHandler} />,
          document.getElementById("backdrop-root")
        )}
        {ReactDOM.createPortal(
          <APIDropdownModal
            setApiPath={setApiPath}
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
}
