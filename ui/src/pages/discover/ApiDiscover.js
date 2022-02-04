import styles from "./apiDiscover.module.css";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
import { DataGrid } from "@material-ui/data-grid";
import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import ReactDOM from "react-dom";
import Backdrop from "../../components/common/Backdrop";
import FileUploadModal from "../../components/fileUpload/FileUploadModal";
import { DeleteOutline } from "@material-ui/icons";
import { targetList } from "../../store/dummyData";

export default function APIInventory() {
  const [data, setData] = useState(targetList);
  const [uploadModalIsOpen, setUploadModalIsOpen] = useState(false);
  const location = useLocation();

  function showModalHandler() {
    setUploadModalIsOpen(true);
  }

  function closeModalHandler() {
    setUploadModalIsOpen(false);
  }

  // const hiddenFileInput = useRef(null);

  // const handleClick = (event) => {
  // hiddenFileInput.current.click();
  // };

  function handleDelete() {}

  const columns = [
    { field: "id", headerName: "ID", width: 100 },
    {
      field: "API Path",
      headerName: "API Path",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "Endpoint URL",
      headerName: "Endpoint URL",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.site}</div>;
      },
    },
    {
      field: "HTTP Method",
      headerName: "HTTP Method",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.lastRun}</div>;
      },
    },
    {
      field: "Collection name",
      headerName: "Collection name",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.lastRun}</div>;
      },
    },
    {
      field: "Added by",
      headerName: "Added by",
      width: 200,
      renderCell: (params) => {
        return <div className="TargetListItem">{params.row.testStatus}</div>;
      },
    },
    {
      field: "OpenAPI Spec",
      headerName: "OpenAPI Spec",
      width: 200,
      renderCell: (params) => {
        return (
          <>
            <Link
              to={{
                pathname: `/apis/spec/editor/`,
                state: { prevPath: location.pathname },
              }}
            >
              <button className="msgListView">Add</button>
            </Link>
            {/* <DeleteOutline
              className="TargetListDelete"
              onClick={() => handleDelete(params.row.id)}
            /> */}
          </>
        );
      },
    },
    {
      field: "Action",
      headerName: "Action",
      width: 150,
      renderCell: (params) => {
        return (
          <>
            {/* <button className="msgListView">Edit</button> */}
            <DeleteOutline
              className="TargetListDelete"
              onClick={() => handleDelete(params.row.id)}
            />
          </>
        );
      },
    },
  ];

  if (uploadModalIsOpen) {
    return (
      <div className="card">
        {ReactDOM.createPortal(
          <Backdrop onCancel={closeModalHandler} />,
          document.getElementById("backdrop-root")
        )}
        {ReactDOM.createPortal(
          <FileUploadModal
            onCancel={closeModalHandler}
            onConfirm={closeModalHandler}
          />,
          document.getElementById("overlay-root")
        )}
      </div>
    );
  } else {
    return (
      <div className="TargetList">
        <div className={topbarStyles.new_action_container}>
          <h1 className="TargetTitle">Discover</h1>
          <div className={styles.import_api_options}>
            {/* <form onSubmit={handleSubmit}> */}
            {/* <input
              type="file"
              onChange={handleChange}
              ref={hiddenFileInput}
              style={{ display: "none" }}
            /> */}
            {/* </form> */}
            <button
              className={buttons.new_action_btn}
              onClick={() => showModalHandler()}
            >
              Import API
            </button>
          </div>
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
