from apscheduler.schedulers.blocking import BlockingScheduler

import GinaTech02.Service as serv
import GinaTech02.Util as util


def us_add_today():
    todaystr = util.get_today_datestr()
    serv.insert_alldaily_oneday_us(todaystr)
def cn_add_today():
    todaystr = util.get_today_datestr()
    serv.insert_alldaily_oneday_cn(todaystr)
def us_predict_today():
    serv.ann_predict_us('cn_2019-07-25_weight.h5')
def cn_predict_today():
    serv.ann_predict_us('us_2019-07-29_weight.h5')

def schedulTask():
    scheduler = BlockingScheduler()
    scheduler.add_job(us_add_today, 'cron', hour=22, minute=45)
    scheduler.add_job(us_predict_today, 'cron', hour=4, minute=10)
    scheduler.add_job(cn_add_today, 'cron', hour=11, minute=10)
    scheduler.add_job(cn_predict_today, 'cron', hour=12, minute=10)
    scheduler.start()



if __name__ == '__main__':

    print("start program...")

    #serv.ann_predict_cn('cn_2019-07-25_weight.h5')
    #serv.ann_predict_us('us_2019-07-14_weight.h5')
    #serv.insert_alldaily_oneday_us('2019-07-25')
    serv.insert_alldaily_oneday_cn('2019-07-29')

    print("end program.")
