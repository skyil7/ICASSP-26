PID=$(pgrep -f "streamlit run webui.py")

# Check if the process is running
if [ -n "$PID" ]; then
    # Terminate the process
    kill $PID
    echo "Streamlit process with PID $PID has been stopped."
else
    echo "No running Streamlit process found."
fi