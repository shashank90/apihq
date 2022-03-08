import os
import json

# from org.parosproxy.paros.model import HistoryReference
# from org.parosproxy.paros.model import Model
# from org.zaproxy.zap.extension.script import ScriptVars

SCRIPT_NAME = "Dump Request"


def sendingRequest(msg, initiator, helper):

    url = msg.getRequestHeader().getURI().toString()
    request_headers = msg.getRequestHeader().toString()
    request_body = msg.getRequestBody().toString()
    request_object = {"headers": request_headers, "body": request_body, "url": url}

    # historyRef = HistoryReference(Model.getSingleton().getSession(), 1, msg)
    # msg.setHistoryRef(historyRef)
    # msg_id = msg.getHistoryRef().getHistoryId()

    headers = msg.getRequestHeader()
    data_dir = headers.getHeader("data_dir")
    request_id = headers.getHeader("request_id")

    file_name = request_id + "_" + "request.json"

    zap_msg_dir = data_dir + "/har/zap_requests"
    try:
        os.makedirs(zap_msg_dir)
    except OSError:
        print(zap_msg_dir + " already exists...")

    file_path = zap_msg_dir + "/" + file_name

    with open(file_path.encode("ascii"), "w") as fp:
        json.dump(request_object, fp)

    # Remove additional request headers
    headers.setHeader("request_id", None)
    headers.setHeader("data_dir", None)


def responseReceived(msg, initiator, helper):
    # historyRef = HistoryReference(Model.getSingleton().getSession(), 1, msg)
    # msg.setHistoryRef(historyRef)
    # msg_id = msg.getHistoryRef().getHistoryId()

    # print("Msg id: " + str(msg_id))
    # value = ScriptVars.getGlobalVar(str(msg_id))
    # print(value)
    # ScriptVars.clearGlobalVar()
    pass
