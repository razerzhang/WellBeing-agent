#!/usr/bin/env python3
"""
Check Recent LangSmith Traces
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langsmith import Client

# Load environment variables
load_dotenv()

def check_recent_traces():
    """Check the most recent traces"""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project_name = os.getenv("LANGCHAIN_PROJECT", "wellbeing-agent")
    
    if not api_key:
        print("❌ LANGCHAIN_API_KEY not found")
        return
    
    client = Client(api_key=api_key)
    
    # Get recent traces (last 2 hours)
    start_time = datetime.now() - timedelta(hours=2)
    
    try:
        traces = list(client.list_runs(
            project_name=project_name,
            start_time=start_time
        ))
        
        print(f"🔍 Recent Traces (Last 2 hours): {len(traces)}")
        print("=" * 50)
        
        for i, trace in enumerate(traces[:5], 1):  # Show last 5 traces
            print(f"\n📊 Trace {i}:")
            print(f"   ID: {trace.id}")
            print(f"   Name: {trace.name}")
            print(f"   Status: {trace.status}")
            print(f"   Start Time: {trace.start_time}")
            print(f"   Duration: {(trace.end_time - trace.start_time).total_seconds():.2f}s" if trace.end_time else "   Duration: Running...")
            
            # Check tags
            if hasattr(trace, 'tags') and trace.tags:
                print(f"   Tags: {trace.tags}")
            
            # Check if it's from production server
            if hasattr(trace, 'tags') and trace.tags and 'production-server' in trace.tags:
                print("   🏭 Source: Production Server")
            else:
                print("   🧪 Source: Test Script")
        
        if len(traces) > 5:
            print(f"\n... and {len(traces) - 5} more traces")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_recent_traces()
