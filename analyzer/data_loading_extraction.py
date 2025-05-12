import pandas as pd

def av_data(path):
    AV_data = pd.read_csv(path)
    log_data = ""

    for i in range(AV_data.shape[0]):
        log_data += (
            f"At {AV_data.loc[i, 'timestamp']}, the car was going at {AV_data.loc[i, 'speed_kph']} kph. "
            f"Brakes engaged: {AV_data.loc[i, 'brake_engaged']}. "
            f"Object detected: {AV_data.loc[i, 'object_detected']}. "
            f"Location: {AV_data.loc[i, 'gps_location']}. "
            f"Acceleration: {AV_data.loc[i, 'acceleration']} m/s². "
            f"Steering angle: {AV_data.loc[i, 'steering_angle_deg']}°. "
            f"Traffic signal: {AV_data.loc[i, 'traffic_signal']}. "
            f"Weather condition: {AV_data.loc[i, 'weather']}. "
            f"Control mode: {AV_data.loc[i, 'control_mode']}.\n\n"
        )

    return log_data
