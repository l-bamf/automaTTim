"""
File schedules the form submission for a certain time in the future (once)
"""
import tt_submit
import schedule
import sys
import time

product_options = {
    "original": "Tim Tam Original",
    "white": "Tim Tam White",
    "dark": "Tim Tam Dark",
    "double": "Tim Tam Double Coat",
    "chewy-caramel": "Tim Tam Chewy Caramel",
    "murray-caramel": "Tim Tam Murray River Salted Caramel"
}


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
