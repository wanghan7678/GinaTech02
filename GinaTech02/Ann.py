import matplotlib.pyplot as plt
from keras import layers
from keras.models import Sequential
from keras.optimizers import RMSprop

import GinaTech02.Config as cfig
import GinaTech02.DataGenerator as dg
import GinaTech02.Usstock_cal as uscal


def create_gru_model():
    model = Sequential()
    model.add(layers.GRU(64,
                         dropout=0.1,
                         recurrent_dropout=0.4,
                         return_sequences=True,
                         input_shape=(None, uscal.FEATURE_NUM)))
    model.add(layers.GRU(128,activation='relu',dropout=0.1,recurrent_dropout=0.4))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer=RMSprop(),loss='binary_crossentropy')
    return model

def train_model(model):
    history = model.fit_generator(dg.train_gen,steps_per_epoch=20,
                                  epochs=5,
                                  validation_data=dg.val_gen,
                                  validation_steps=dg.val_steps)
    return history


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

def load_model(filepath):
    model = load_model(filepath)
    return model

def predict_model(model):
    arr = dg.get_predictlist()
    samples = arr[0]
    symbols = arr[1]
    pred = model.predict(samples)
    return [pred, symbols]