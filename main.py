import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

import os
from acconeer.exptool import a121
from sklearn.model_selection import train_test_split
import argparse

import pickle as pkl

from sklearn.decomposition import PCA

from models import basemodel, acconeer

from preprocess import processing

idx2label_Dict = {
    0 : 'asphalt',
    # 1 : 'bicycle',
    1 : 'brick',
    2 : 'tile',
    3 : 'sandbed',
    4 : 'urethane',
}

def saveplot(history, plot_name):
    plot_name =  str(plot_name) + '.png'
    plt.subplot(4,1,1)
    plt.ylim(0,1)
    max = np.argmax(history['val_accuracy'])
    plt.plot(history['val_accuracy'])
    plt.plot(max, history['val_accuracy'][max], 'o', ms = 10, label=round(history['val_accuracy'][max],4))
    plt.title('val_accuracy')
    plt.legend(loc = 'center right',fontsize=15)

    plt.subplot(4,1,2)
    plt.ylim(0,1)
    min = np.argmin(history['val_loss'])
    plt.plot(history['val_loss'])
    plt.plot(min, history['val_loss'][max], 'o', ms = 10, label=round(history['val_loss'][max],4))
    plt.title('val_loss')
    plt.legend(loc = 'center right',fontsize=15)

    plt.subplot(4,1,3)
    plt.ylim(0,1)
    max = np.argmax(history['accuracy'])
    plt.plot(history['accuracy'])
    plt.plot(max, history['accuracy'][max], 'o', ms = 10, label=round(history['accuracy'][max],4))
    plt.title('accuracy')
    plt.legend(loc = 'center right',fontsize=15)

    plt.subplot(4,1,4)
    plt.ylim(0,1)
    min = np.argmin(history['loss'])
    plt.plot(history['loss'])
    plt.plot(min, history['loss'][max], 'o', ms = 10, label=round(history['loss'][max],4))
    plt.title('loss')
    plt.legend(fontsize=15)
    plt.legend(loc = 'center right',fontsize=15)
    plt.savefig(plot_name, dpi = 300)
    
# def saveplot(history, plot_name):
#     plot_name =  str(plot_name) + '.png'
#     # plt.subplot(2,1,1)
#     plt.figure(figsize=(12,5))
#     plt.ylim(0,1)
#     max = np.argmax(history['val_accuracy'])
#     plt.plot(history['val_accuracy'])
#     plt.plot(max, history['val_accuracy'][max], 'o', color = 'k', ms = 10, label=('max acc : ' + str(round(history['val_accuracy'][max],4))))
#     plt.title('test accuracy')
#     plt.legend(loc = 'center right',fontsize=15)
#     plt.savefig(plot_name, dpi = 300)

def mean_data(pca = False):
    preprocess = processing()
    preprocess.make_norm_mean_frame()
    if pca:
        title = 'mean_data_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.norm_mean_data, 'pca/mean_pca.pkl')), title
    else:
        title = 'mean_data'
        return preprocess.make_ds(preprocess.norm_mean_data), title

def mean_norm_of_data(pca = False):
    preprocess = processing()
    preprocess.make_norm_mean_frame()
    if pca:
        title = 'mean_norm_data_pca'
        return preprocess.make_ds(preprocess.norm_mean_data), title
    else:
        title = 'mean_norm_data'
        return preprocess.make_ds(preprocess.norm_mean_data)

def var_data(pca = False):
    preprocess = processing()
    preprocess.make_var_frame()
    if pca:
        title = 'var_data_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.var_data, 'pca/var_pca.pkl')), title
    else :
        title = 'var_data'
        return preprocess.make_ds(preprocess.var_data), title

def diff_mean_frame(pca = False):
    preprocess = processing()
    preprocess.mean_of_frame_diff()
    if pca:
        title = 'mean_of_frame_diff_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.diff_frame_mean, 'pca/diff_mean_pca.pkl')), title
    else:
        title = 'mean_of_frame_diff'
        return preprocess.make_ds(preprocess.diff_frame_mean), title

def diff_var_frame(pca = False):
    preprocess = processing()
    preprocess.var_of_frame_diff()
    if pca:
        title = 'diff_var_frame_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.diff_frame_var, 'pca/diff_var_pca.pkl')), title
    else:
        title = 'diff_var_frame'
        return preprocess.make_ds(preprocess.diff_frame_var), title

def diff_mean_dist(pca = False):
    preprocess = processing()
    preprocess.diff_mean_dist()
    if pca:
        title = 'diff_mean_dist_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.diff_mean_of_dist, 'pca/diff_dist_mean_pca.pkl')), title
    else:
        title = 'diff_mean_dist'
        return preprocess.make_ds(preprocess.diff_mean_of_dist), title

def diff_var_dist(pca = False):
    preprocess = processing()
    preprocess.diff_var_dist()
    if pca:
        title = 'diff_var_dist_pca'
        return preprocess.make_ds(preprocess.pca_data(preprocess.diff_var_of_idst, 'pca/diff_dist_var_pca.pkl')), title
    else:
        title = 'diff_var_dist'
        return preprocess.make_ds(preprocess.diff_var_of_dist), title

def mean_var_data(pca = False):
    preprocess = processing()
    preprocess.make_norm_mean_frame()
    preprocess.make_norm_of_var_data()
    concat_data = preprocess.data_concat(preprocess.norm_mean_data, preprocess.norm_of_var_data)
    if pca:
        title = 'concat_mean_var_pca'
        return preprocess.make_ds(preprocess.pca_data(concat_data, 'pca/mean_var_pca.pkl')), title
    else:
        title = 'concat_mean_var'
        return preprocess.make_ds(concat_data), title

def mean_var_norm_data(pca = False):
    preprocess = processing()
    # preprocess.make_norm_mean_frame()
    preprocess.make_mean_of_norm_data()
    preprocess.make_var_of_norm_data()
    # concat_data = preprocess.data_concat(preprocess.norm_mean_data, preprocess.var_of_norm_data)
    concat_data = preprocess.data_concat(preprocess.mean_of_norm_data, preprocess.var_of_norm_data)
    if pca:
        title = 'concat_mean_var_norm_pca'
        return preprocess.make_ds(preprocess.pca_data(concat_data, 'pca/mean_var_pca.pkl')), title
    else:
        title = 'concat_mean_var'
        return preprocess.make_ds(concat_data), title

def acconeer_data(pca = False):
    # title = 'acconeer_data'
    preprocess = processing()
    autocov = preprocess.autocovdict()
    # print('autocovariance shape : ', autocov['asphalt'].shape)
    concat_Data = preprocess.data_concat(preprocess.mean_data, autocov)
    if pca:
        title = 'acconeer_data_pca'
        return preprocess.make_ds(preprocess.pca_data(concat_Data, 'pca/acconeer.pkl')), title
    
    else:
        title = 'acconeer_data'
        return preprocess.make_ds(concat_Data), title
    # print('concat data shape : ', concat_Data['asphalt'].shape)
    # Data = preprocess.make_ds(concat_Data)
    # return Data, title
    # preprocess.

def make_log(y, y_pred):
    Y = np.argmax(y, axis = 1)
    Y_pred = np.argmax(y_pred, axis = 1)
    log_y = [idx2label_Dict[Y[i]] for i in range(len(Y))]
    log_y_pred = [idx2label_Dict[Y_pred[i]] for i in range(len(Y_pred))]
    arr = np.array([log_y, log_y_pred])
    df = pd.DataFrame(arr)
    df.index = ['Ground Truth', 'Prediction']
    df.to_csv('./report_log.csv')

def train(
    model, X, Y,
    test_X, test_Y, 
    # callback,
    Epoch = 50,
    learning_rate = 1e-3,
    cp_path = None,
    ):
    callback = tf.keras.callbacks.ModelCheckpoint(
        filepath = './model/' + cp_path,
        monitor='val_accuracy',
        mode='max',
        save_best_only = True,
        save_weigths_only = False,
    )
    optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate)
    loss = tf.keras.losses.CategoricalCrossentropy()
    model.compile(optimizer = optimizer , loss = loss, 
                metrics = ['accuracy', 'categorical_crossentropy'])
    print('X shape : ', X.shape)
    model.build(input_shape = (1, X.shape[1]))          
    model.summary()
    history = model.fit(X, Y,  epochs = Epoch,
                validation_data = (test_X, test_Y),
                callbacks = [callback]
                )
    return history

def main():
    
    parser = argparse.ArgumentParser(description = 'selt data and gpu')
    parser.add_argument('-g', '--gpu', action = 'store', default = '3')
    parser.add_argument('-p', '--pca', action = 'store_true')
    parser.add_argument('-d', '--data', action = 'store')
    parser.add_argument('-m', '--model', action = 'store', default = 'base')
    args = parser.parse_args()

    gpu = int(args.gpu)
    data = args.data
    Pca = args.pca
    sel_model = args.model
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
    # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
        try:
            tf.config.experimental.set_visible_devices(gpus[gpu], 'GPU')
            tf.config.experimental.set_virtual_device_configuration(
                gpus[gpu],
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=10240)])
        except RuntimeError as e:
            # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
            print(e)

    if data == 'mean_data':
        DATA, title = mean_data(Pca)
    elif data == 'var_data':
        DATA, title = var_data(Pca)
    elif data == 'diff_mean_frame':
        DATA, title = diff_mean_frame(Pca)
    elif data == 'diff_var_frame' :
        DATA, title = diff_var_frame(Pca)
    elif data == 'diff_mean_dist':
        DATA, title = diff_mean_dist(Pca)
    elif data == 'diff_var_dist':
        DATA, title = diff_var_dist(Pca)
    elif data == 'acconeer':
        DATA, title = acconeer_data(Pca)
    elif data == 'mean_var':
        DATA, title = mean_var_data(Pca)
    elif data == 'mean_var_norm':
        DATA, title = mean_var_norm_data(Pca)
    else :
        'error'
    
    X_train, Y_train, X_test, Y_test = DATA[0], DATA[2], DATA[1], DATA[3]

    if sel_model == 'base':
        title = './basemodel/' + title
        model = basemodel()
        history = train(model, X_train, Y_train, X_test, Y_test, Epoch = 50, cp_path=title)
        saveplot(history.history, title)
    elif sel_model == 'acconeer':
        title = './acconeer/' + title
        model = acconeer()
        history = train(model, X_train, Y_train, X_test, Y_test, Epoch = 50, cp_path=title)
        saveplot(history.history, title)
    elif sel_model == 'predict':
        path = 'model/basemodel/concat_mean_var_norm_pca'
        model = tf.keras.models.load_model(path)
        y_pred = model.predict(X_test)
        make_log(Y_test, y_pred)
if __name__ == '__main__':
    main()