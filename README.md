# ext_ip
Checks whether the external ip address of the home network has changed. 

For the SMS notification, [clicksend.com](https://dashboard.clicksend.com/home) is used. Create a free account to use free credit then topup when needed.

For orchestration, [app.prefect.cloud](https://app.prefect.cloud) is used. Create a free hobbyist account, and observe the limits of this when scheduling flows. An API key is used when logging into prefect from the terminal (cli).

## Setup
1. Install python (if not already present)
1. Create your prefect venv e.g. `python -m venv prefect` 
1. Activate e.g. `.\prefect\scripts\activate`
1. Ensure pip is updated e.g. `python -m pip install --upgrade pip`
1. Fetch down the repo contents e.g. `git clone https://github.com/dmonlineuk/ext_ip.git`
1. Install requirements e.g. `cd ext_ip ; pip install -r .\requirements.txt`
1. Log into prefect e.g. `prefect cloud login`
1. Set up a `.env` file, with the following information relating to your clicksend account:
```.env
API_KEY=xxxx
USERNAME=xxx@xxx.xx
TO_NUMBER=+441234567890
```
9. Run the script e.g. `python .\main.py`
Note this holds the thread while the prefect flow is served, while the Prefect UI is used to schedule or run actual flow runs; ctrl+c will stop this

## Advanced - Background served flows
1. Ensure you are authorised for prefect cloud e.g. `prefect cloud login`
1. Create a batch file similar to the following
```cmd
cd C:\Users\myself\projects\prefect\ext_ip\
call ..\Scripts\activate.bat
python main.py
```
3. Set up a scheduled task to run this batch file. Maybe set it so it re-run in case of failure or every 5 minutes.
Note the flow does not run as per any schedule you set in the OS, rather as before it should run and hold its thread in the background, while the Prefect UI is used to schedule or run actual flow runs
 