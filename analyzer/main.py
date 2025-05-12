from data_loading_extraction import av_data
from incident_analyzer import get_API_key, create_incident_agent, run_agent

data_path="data/av_rich_incident_log.csv"
log_data=av_data(data_path)
api_key=get_API_key()
agent=create_incident_agent(api_key)
print(run_agent(log_data, agent))