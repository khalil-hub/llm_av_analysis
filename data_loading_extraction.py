import pandas as pd
def av_data(path):
    AV_data=pd.read_csv(path)
    print(AV_data)
    log_data = ""
    for i in range(AV_data.shape[0]):
        log_data += (
            "At " + str(AV_data.loc[i, "timestamp"]) +
            " the car was going at " + str(AV_data.loc[i, "speed_kph"]) + " kph. " +
            "Brakes engaged: " + str(AV_data.loc[i, "brake_engaged"]) + ". " +
            "Object detected: " + str(AV_data.loc[i, "object_detected"]) + ". " +
            "Location: " + str(AV_data.loc[i, "gps_location"]) + "\n\n"
        )

    return log_data
