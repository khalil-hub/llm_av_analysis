from data_loading_extraction import av_data
from incident_summarizer import get_API_key, incident_summary, run_summary
AV_path="data/av_incident_log.csv"
av_string=av_data(AV_path)
get_API_key()
chain=incident_summary()
print(run_summary(av_string, chain))