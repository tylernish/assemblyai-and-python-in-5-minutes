from apscheduler.schedulers.blocking import BlockingScheduler
import send_func

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=300)
def timed_job():
    print('This job is run every 10 minutes.')
    ##Here I can make it check if there are any incomplete rows with send_func.updateSheetData()
    send_func.main()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10)
def scheduled_job():
    print('This job is run every weekday at 10am.')

##sched.configure(options_from_ini_file)

sched.start()
##CTRL+C to stop