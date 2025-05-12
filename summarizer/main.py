from summarizer.data_loading_extraction import av_data
from summarizer.incident_summarizer import get_API_key, incident_summary, run_summary
AV_path="data/av_incident_log.csv"
av_string=av_data(AV_path)
llm=get_API_key()
chain=incident_summary(llm)
print(run_summary(av_string, chain))