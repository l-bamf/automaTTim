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


def delayed_entry(type="original"):
    tt_submit.full_flow(type)
    return schedule.CancelJob


if __name__ == "__main__":
    scheduled_time = ""
    if len(sys.argv) > 1:
        scheduled_time = sys.argv[1]
    else:
        scheduled_time = "15:13"

    if len(sys.argv) > 2:
        if sys.argv[2] in product_options:
            schedule.every().day.at(scheduled_time).do(delayed_entry, type=sys.argv[2])
        else:
            print("Invalid product type as argument - must be one of: ")
            print(product_options.keys())
            exit()
    else:
        schedule.every().day.at(scheduled_time).do(delayed_entry)
    print("Waiting for " + scheduled_time + "...")
    while True:
        schedule.run_pending()
        time.sleep(1)
