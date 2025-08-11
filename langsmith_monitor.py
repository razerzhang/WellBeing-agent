#!/usr/bin/env python3
"""
LangSmith Monitor
Monitor and analyze traces from the Wellbeing Agent
"""

import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langsmith import Client

# Load environment variables
load_dotenv()

class LangSmithMonitor:
    def __init__(self):
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        self.project_name = os.getenv("LANGCHAIN_PROJECT", "wellbeing-agent")
        
        if not self.api_key:
            raise ValueError("LANGCHAIN_API_KEY not found")
        
        self.client = Client(api_key=self.api_key)
    
    def get_recent_traces(self, hours: int = 24):
        """Get recent traces from the last N hours"""
        start_time = datetime.now() - timedelta(hours=hours)
        
        try:
            traces = list(self.client.list_runs(
                project_name=self.project_name,
                start_time=start_time
            ))
            return traces
        except Exception as e:
            print(f"❌ Error fetching traces: {e}")
            return []
    
    def analyze_traces(self, traces):
        """Analyze traces and return statistics"""
        if not traces:
            return {"error": "No traces found"}
        
        stats = {
            "total_traces": len(traces),
            "successful_traces": 0,
            "failed_traces": 0,
            "avg_duration": 0
        }
        
        total_duration = 0
        
        for trace in traces:
            if trace.error:
                stats["failed_traces"] += 1
            else:
                stats["successful_traces"] += 1
            
            if trace.start_time and trace.end_time:
                duration = (trace.end_time - trace.start_time).total_seconds()
                total_duration += duration
        
        if stats["total_traces"] > 0:
            stats["avg_duration"] = total_duration / stats["total_traces"]
        
        return stats
    
    def print_analysis(self, stats):
        """Print analysis results"""
        print("\n📊 LangSmith Analysis Report")
        print("=" * 50)
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
            return
        
        print(f"📈 Total Traces: {stats['total_traces']}")
        print(f"✅ Successful: {stats['successful_traces']}")
        print(f"❌ Failed: {stats['failed_traces']}")
        print(f"⏱️  Average Duration: {stats['avg_duration']:.2f}s")

async def main():
    """Main function"""
    print("🔍 LangSmith Monitor")
    print("=" * 30)
    
    try:
        monitor = LangSmithMonitor()
        
        # Get recent traces
        print(f"🔍 Fetching recent traces from '{monitor.project_name}'...")
        traces = monitor.get_recent_traces(hours=24)
        
        if traces:
            print(f"✅ Found {len(traces)} traces in the last 24 hours")
            stats = monitor.analyze_traces(traces)
            monitor.print_analysis(stats)
        else:
            print("ℹ️  No traces found in the last 24 hours")
        
        print(f"\n🌐 View traces at: https://smith.langchain.com/")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
