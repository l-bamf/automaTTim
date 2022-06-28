"""
File schedules the form submission for a certain time in the future (once)
"""
import tt_submit
import schedule
import sys
import time

retailer_options = {
    "coles": "Coles-1",
    "woolworths": "Woolworths-1",
    "iga": "IGA",
    "countdown": "Countdown-1",
    "new-world": "New World-1",
    "paknsave": "Pak'nSave",
    "other": "Other-3"
}


def delayed_entry():
    tt_submit.full_flow()
    return schedule.CancelJob


if __name__ == "__main__":
    scheduled_time = ""
    if len(sys.argv) == 2:
        scheduled_time = sys.argv[1]
    else:
        scheduled_time = "15:13"

    receipt, flavour, retailer = tt_submit.find_receipt()
    if not receipt:
        print("No valid receipt found. Please ensure photo is in correct folder and of type jpg,jpeg,pdg,png")
    else:
        schedule.every().day.at(scheduled_time).do(delayed_entry)
        print("Will submit at next occurrence of " + scheduled_time + "...")
        if retailer == "coles" and "coles" not in receipt:
            print("Assumed retailer is Coles (default), to specify a different retailer please add to receipt file name valid retailer string: ")
            print(str(list(retailer_options.keys())))

        while True:
            schedule.run_pending()
            time.sleep(1)
            # cancel when job is finished
            if len(schedule.get_jobs()) == 0:
                time.sleep(15)
                exit()
