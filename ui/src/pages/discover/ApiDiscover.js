import styles from "./apiDiscover.module.css";
import topbarStyles from "../../components/common/topbarstyles.module.css";
import buttons from "../../components/common/buttons.module.css";
import { DataGrid } from "@material-ui/data-grid";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect, useCallback, useContext } from "react";
import ReactDOM from "react-dom";
import Backdrop from "../../components/common/Backdrop";
import AddApiModal from "../../components/addApi/AddApiModal";
import { DeleteOutline } from "@material-ui/icons";
import AuthContext from "../../store/auth-context";

const getApisURL = "http://localhost:3000/apis/v1/discovered";

export default function APIInventory() {
  const [apis, setApis] = useState([]);
  const [uploadModalIsOpen, setUploadModalIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const location = useLocation();
  const authCtx = useContext(AuthContext);

  function showModalHandler() {
    setUploadModalIsOpen(true);
  }

  function closeModalHandler() {
    setUploadModalIsOpen(false);
  }

  function handleDelete() {}

  const fetchApisHandler = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(getApisURL, {
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
      }

      const transformedApis = data.apis.map((api, index) => {
        return {
          id: index + 1,
          specId: api.spec_id,
          apiPath: api.api_path,
          // endpointURL: api.endpoint_url,
          httpMethod: api.http_method,
          // status: api.status,
          addedBy: api.added_by,
        };
      });
      setApis(transformedApis);
    } catch (error) {
      setError(error.message);
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    fetchApisHandler();
  }, [fetchApisHandler]);

  const columns = [
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "API Path",
      headerName: "API Path",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.apiPath}</div>
        );
      },
    },
    {
      field: "Endpoint URL",
      headerName: "Endpoint URL",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.apiPath}</div>
        );
      },
    },
    {
      field: "HTTP Method",
      headerName: "HTTP Method",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.httpMethod}</div>
        );
      },
    },
    {
      field: "Status",
      headerName: "Status",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.addedBy}</div>
        );
      },
    },
    {
      field: "Added by",
      headerName: "Added by",
      width: 200,
      renderCell: (params) => {
        return (
          <div className={styles.TargetListItem}>{params.row.addedBy}</div>
        );
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
                pathname: `/apis/spec/editor/${params.row.specId}`,
                state: { prevPath: location.pathname },
              }}
            >
              <button className={styles.msgListView}>View</button>
            </Link>
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
              className={styles.TargetListDelete}
              onClick={() => handleDelete(params.row.id)}
            />
          </>
        );
      },
    },
  ];

  let content = (
    <DataGrid
      rows={apis}
      disableSelectionOnClick
      columns={columns}
      pageSize={8}
      checkboxSelection
    />
  );

  if (error) {
    content = <p>{error}</p>;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

  if (uploadModalIsOpen) {
    return (
      <div className="card">
        {ReactDOM.createPortal(
          <Backdrop onCancel={closeModalHandler} />,
          document.getElementById("backdrop-root")
        )}
        {ReactDOM.createPortal(
          <AddApiModal
            onCancel={closeModalHandler}
            onConfirm={closeModalHandler}
          />,
          document.getElementById("overlay-root")
        )}
      </div>
    );
  } else {
    return (
      <div className={styles.TargetList}>
        <div className={topbarStyles.new_action_container}>
          <h1 className={styles.TargetTitle}>Discover</h1>
          <div className={styles.import_api_options}>
            <button
              className={buttons.new_action_btn}
              onClick={() => showModalHandler()}
            >
              Import API
            </button>
          </div>
        </div>
        {content}
      </div>
    );
  }
}
