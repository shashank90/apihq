import zapv2

from log.factory import Logger

logger = Logger(__name__)


def get_alerts(zap: zapv2, target: str):
    # Retrieve the alerts using paging in case there are lots of them
    st = 0
    pg = 5000
    alert_dict = {}
    alert_count = 0
    alerts = zap.alert.alerts(baseurl=target, start=st, count=pg)
    blacklist = [1, 2]
    while len(alerts) > 0:
        print("Reading " + str(pg) + " alerts from " + str(st))
        alert_count += len(alerts)
        for alert in alerts:
            plugin_id = alert.get("pluginId")
            if plugin_id in blacklist:
                continue
            if alert.get("risk") == "High":
                # Trigger any relevant postprocessing. For now just add them to alert_dict
                print(alert)
                continue
            if alert.get("risk") == "Informational":
                # Ignore all info alerts - some of them may have been downgraded by security annotations
                continue
        st += pg
        alerts = zap.alert.alerts(start=st, count=pg)
    print("Total number of alerts: " + str(alert_count))


if __name__ == "main":
    get_alerts(zapv2, target="http://localhost:3000")
