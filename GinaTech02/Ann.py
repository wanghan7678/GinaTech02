import matplotlib.pyplot as plt
from keras import layers
from keras.models import Sequential
from keras.optimizers import RMSprop

import GinaTech02.Config as cfig
import GinaTech02.DataGenerator as dg
import GinaTech02.Stock_cal as scal
import GinaTech02.Util as util


def create_gru_model():
    model = Sequential()
    model.add(layers.GRU(64,
                         dropout=0.1,
                         recurrent_dropout=0.4,
                         return_sequences=True,
                         input_shape=(None, scal.FEATURE_NUM)))
    model.add(layers.GRU(128,activation='relu',dropout=0.1,recurrent_dropout=0.4))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=RMSprop(),loss='binary_crossentropy')
    return model

def train_model(model, train_gen, val_gen):
    history = model.fit_generator(train_gen,steps_per_epoch=300,
                                  epochs=20,
                                  validation_data=val_gen,
                                  validation_steps=5)
    return history


def train_model_us(model):
    his = train_model(model, train_gen=dg.train_gen_us, val_gen=dg.val_gen_us)
    return his

def train_model_cn(model):
    his = train_model(model, train_gen=dg.train_gen_cn, val_gen=dg.val_gen_cn)
    return his


def draw_plot(history):
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(loss)+1)

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation acc')
    plt.legend()
    plt.show()

def save_model(model):
    mdfilename = cfig.model_filepath()
    wtfilename = cfig.weights_filepath()
    model.save_weights(wtfilename, overwrite=True)
    model.save(mdfilename)

def save_model2(model, filename):
    mdf = filename+"_"+util.get_today_datestr()+"_model.h5"
    wtf = filename+"_"+util.get_today_datestr()+"_weight.h5"
    model.save_weights(wtf, overwrite=True)
    model.save(mdf)


def predict_model_us(model):
    arr = dg.get_predictlist_us()
    samples = arr[0]
    symbols = arr[1]
    print("start predict: total %d samples." %len(samples))
    pred = model.predict(samples)
    print("finish predict.  predict: "+str(len(pred))+", symbols: "+str(len(symbols)))
    return [pred, symbols]

def predict_model_cn(model):
    arr = dg.get_predictlist_cn()
    samples=arr[0]
    symbols = arr[1]
    print("start predict: total %d samples." %len(samples))
    pred = model.predict(samples)
    print("finish predict.  predict: "+str(len(pred))+", symbols: "+str(len(symbols)))
    return [pred, symbols]