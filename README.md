# AutomaTTim
Using my software skills for [evil](https://www.youtube.com/watch?v=MNt3-rX6pbo)...

## Premise
Arnotts is currently running a promotional campaign
wherein three specially marked TimTam packets contain a little lamp worth one wish ($100,000), ala Aladdin.
You may, like me, better associate this marketing strategy with a franchise 
unrelated to genies but this section of the promotion can be ignored just like the Johnny Depp version.

The more important competition and the one this tool is built to exploit is a giveaway of $100 hourly to
anyone who fills out an online application in the previous hour. 
This occurs every hour of the day, **including late at night**. 
So, the simple calculation is that few enough people will apply during these hours to make the price of
a packet a greater than break-even investment. 
The magic number for the hour is either 25 entrants for full price ($4) or 50 for half price ($2).
Since the campaign is only is Australia and New Zealand, it's plausible that during a couple of hours
the participation will drop below this number.
Profit is the goal but increasing my odds means, in the worst case, a packet is nicely subsidised.

Of course, I don't actually want to apply during those hours (hopefully nobody does) so the goal of this project is 
to automate submission while I sleep.

![alt text](https://i.pinimg.com/736x/e8/e7/4d/e8e74d6f2218e8c7a0f138b9e2d6ff9a.jpg)

# Installation
## Cloning
The repository can be cloned to your local machine by running in command line. It can also be directly downloaded from
GitHub/

    git clone https://github.com/l-bamf/automaTTim
## Dependencies
#### Browser
This project depends on Chrome Version 103.0.5060.66 (Official Build) (64-bit) being installed in the default directory.
This is the version the project's chromedriver expects.
#### Python
The Python files were written and tested with 3.10.4. [Install Python](https://www.python.org/downloads/)
#### Python Libraries
A couple libraries need to be installed

    pip install selenium
    pip install schedule
#### Hardware
I haven't tested the hardware requirements at all but from my reading the machine needs an internet connection
and to run *not in sleep* until the selected time

#### details.json
Rename details_schema.json to details.json and fill in your relevant details in the same format.

#### timtam3wishes.com
I doubt this website will continue to be maintained, or even exist, after the promotional period ends (3/7/22)

# Execution
Before executing the script, put an image of your receipt into the receipts folder. Original should be left in the top
receipts\ but other flavours should be put in their respective folder. For receipts with multiple products, it is fine
to duplicate these as many times as were purchased, as far as I'm aware. Each entry requires and consumes one receipt file.
Steps are as follows:
1. Update details.json file if not already done
2. Place photo of receipt in relevant flavour folder
3. Add retailer string to filename if required
4. Run command line

## Instant submission
If you wish to instantly submit the form run

    python tt_sumbit.py
    
## Delayed submission
This is the core use-case of delaying submission to a lonely time of night. This runs the submission once at the 
next occurrence of the specified time.

    python tt_time.py HH:MM
    python tt_time.py 03:11

## Specific flavours
To accommodate for different flavours being bought, place the receipt in the relevant receipt folder. The program will
dynamically recognise the flavour from a receipt's location; there is no need to explicitly state it.

## Specific retailers
The default retailer is Coles. To specify a different retailer add one of the valid strings to anywhere in your receipt file name: 
['coles', 'woolworths', 'iga', 'countdown', 'new-world', 'paknsave', 'other'].
 
    original\image_67206913  # default (Coles) 
    original\igaimage_67206913  # IGA
    original\image_67206913other  # Other

# Results
I have won only once, but I have still made a profit so far.

| Hour      | Submissions | Wins |
| ----------- | ----------- | ------|
| 02:01     | 2       | 0 |
| 03:01   | 8        | 0 |
| 04:01   | 5        | 1 |
