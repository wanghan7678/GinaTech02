import GinaTech02.Service as serv

if __name__ == '__main__':

    print("start program...")

    #serv.ann_predict_cn('cn_2019-07-25_weight.h5')
    serv.ann_predict_us('us_2019-07-14_weight.h5')
    #serv.insert_alldaily_oneday_us('2019-07-25')
    #serv.insert_alldaily_oneday_cn('2019-07-26')

    print("end program.")
