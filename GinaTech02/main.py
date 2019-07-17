import GinaTech02.Service as serv

if __name__ == '__main__':

    print("start program...")

    #serv.ann_predict_us('us__2019-07-14_weight.h5')

    #serv.insert_cnstock_all()
    serv.insert_alldaily_oneday_cn('2019-07-15')

    print("end program.")
