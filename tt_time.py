"""
File schedules the form submission for a certain time in the future (once)
"""
import tt_submit
import schedule
import sys
import time

def delayed_entry():
    tt_submit.full_flow()
    return schedule.CancelJob


if __name__ == "__main__":
    scheduled_time = ""
    if len(sys.argv) > 1:
        scheduled_time = sys.argv[1]
    else:
        scheduled_time = "15:13"

    schedule.every().day.at(scheduled_time).do(delayed_entry)
    print("Waiting for " + scheduled_time + "...")
    while True:
        schedule.run_pending()
        time.sleep(1)
