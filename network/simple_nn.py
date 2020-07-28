import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
import tensorflow
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from tensorflow_core.python.keras.layers import Dense
from tensorflow_core.python.keras.utils import np_utils
from tensorflow_core.python.keras.wrappers.scikit_learn import KerasClassifier

from network import read_datasets
from tensorflow.keras.optimizers import SGD

from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split


from sklearn.metrics import confusion_matrix


def plots(history):
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


def simple_nn_1():
    path = '../datasets/center_distance/vectors_2/window_size_11/10steps_5walks/data1_100.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)
    # train_data, train_labels, test_data, test_labels = read_datasets.read_from_json()
    # train_data, train_labels, test_data, test_labels = read_datasets.read_from_csv()

    # print("train_data ", str(type(train_data)), " size ", train_data.shape, " ", train_data[0])
    # print("train_labels ", str(type(train_labels)), " size ", train_labels.shape)
    # print(np.unique(train_labels))
    # print("test_data ", str(type(test_data)), " size ", test_data.shape)
    # print("test_labels ", str(type(test_labels)), " size ", test_labels.shape)
    # print(np.unique(test_labels))

    model = Sequential([
        keras.layers.Dense(20, input_shape=(input_shape_x,), activation="relu"),
        keras.layers.Dense(160, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])

    model.summary()

    opt1 = Adam(learning_rate=.0001)
    # opt2 = SGD(learning_rate=0.001)
    # opt3 = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    history = model.fit(train_data, train_labels, batch_size=64, epochs=3, shuffle=True,
                        class_weight=classWeight,
                        validation_split=0.1,
                        verbose=2)
    #
    # model.evaluate(x=test_data, y=test_labels)
    plots(history)
    # exit(0)


def simple_nn_2():
    # from sklearn.utils import compute_class_weight
    # classWeight = compute_class_weight('balanced', outputLabels, outputs)
    # classWeight = dict(enumerate(classWeight))
    # model.fit(X_train, y_train, batch_size = batch_size, nb_epoch = nb_epochs, show_accuracy = True, verbose = 2, \
    #           validation_data = (X_test, y_test), class_weight=classWeight)

    path = '../datasets/center_distance/vectors_2/window_size_11/10steps_5walks/data1_100.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(20, input_shape=(input_shape_x,), activation="relu"),
        keras.layers.Dense(160, activation="relu"),
        # keras.layers.Dense(400, activation="relu"),
        # keras.layers.Dense(160, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.0001)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=8, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)

    # exit(1)


def simple_nn_3():
    path = '../datasets/center_distance/vectors_2/window_size_11/10steps_5walks/data0_50.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(218, input_shape=(input_shape_x,), activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.000094878)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    history = model.fit(train_data, train_labels, batch_size=41, epochs=40, shuffle=True,
                        class_weight=classWeight,
                        validation_split=0.1,
                        verbose=2)
    plots(history)


def simple_nn_4():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(512, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.0001)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=64, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_5():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_6():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_7():
    path = '../datasets/center_distance/vectors_1/window_size_11/2steps_10walks/data4_60.csv'
    train_data, train_labels = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(60,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              # class_weight=classWeight,
              # validation_split=0.1,
              verbose=2)


def simple_nn_8():
    path = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/10steps_5walks/data2_200.csv'
    # path = '../datasets/center_distance/vectors_1/window_size_31/10steps_5walks/data2_200.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)
    x_test = train_data[-100:]
    x_train = train_data[:-100]
    y_test = train_labels[-100:]
    y_train = train_labels[:-100]

    x_val = x_train[-1000:]
    y_val = y_train[-1000:]
    x_train = x_train[:-1000]
    y_train = y_train[:-1000]

    model = Sequential([
        keras.layers.Dense(218, input_shape=(input_shape_x,), activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.000094878)
    opt2 = SGD(lr=0.01)
    opt3 = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    history = model.fit(x_train, y_train, batch_size=64, epochs=200, shuffle=True,
                        # class_weight=classWeight,
                        # validation_split=0.1,
                        validation_data=(x_val, y_val),
                        verbose=2)

    # # Evaluate the model on the test data using `evaluate`
    # print("Evaluate on test data")
    # results = model.evaluate(x_test, y_test, batch_size=128)
    # print("test loss, test acc:", results)

    # Y_test = np.argmax(y_test, axis=1)  # Convert one-hot to index
    y_pred = model.predict_classes(x_test)
    # target_names = [i for i in range(0, 15)]
    print(classification_report(y_test, y_pred))
    return history


def simple_nn_9():
    path = '../datasets/center_distance/vectors_1/window_size_31/10steps_5walks/data2_200.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)

    X = train_data.astype(float)
    Y = train_labels

    # encode class values as integers
    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    # define baseline model
    def baseline_model():
        # create model
        model = Sequential()
        model.add(Dense(8, input_dim=input_shape_x, activation='relu'))
        model.add(Dense(15, activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    estimator = KerasClassifier(build_fn=baseline_model, epochs=20, batch_size=5, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, X, dummy_y, cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))


def simple_nn_10():
    path = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/2steps_10walks/data0_20.csv'
    train_data, train_labels, input_shape_x = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(input_shape_x,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              # class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_11():
    path = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/10steps_5walks/data0_50.csv'
    x, y, input_shape_x = read_datasets.read_data(path)
    # Split into train/test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42)

    model = Sequential()
    print(" ----------------------------- ", x.shape[1])
    model.add(Dense(100, input_dim=x.shape[1], activation='relu',
                    kernel_initializer='random_normal'))
    model.add(Dense(50, activation='relu', kernel_initializer='random_normal'))
    model.add(Dense(25, activation='relu', kernel_initializer='random_normal'))
    model.add(Dense(15, activation='softmax',
                    kernel_initializer='random_normal'))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tensorflow.keras.optimizers.Adam(),
                  metrics=['accuracy'])
    monitor = EarlyStopping(monitor='val_loss', min_delta=1e-3, patience=5,
                            verbose=1, mode='auto', restore_best_weights=True)

    model.fit(x_train, y_train, validation_data=(x_test, y_test),
              # callbacks=[monitor],
              verbose=2, epochs=1000)


def scikit_cla():
    path = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/10steps_5walks/data0_50.csv'
    x, y, input_shape_x = read_datasets.read_data(path)
    # Split into train/test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42)



    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

    # training a KNN classifier
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train)

    # accuracy on X_test
    accuracy = knn.score(X_test, y_test)
    print(accuracy)

    # creating a confusion matrix
    knn_predictions = knn.predict(X_test)
    cm = confusion_matrix(y_test, knn_predictions)


from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def nb():
    path = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/10steps_5walks/data0_50.csv'
    x, y, input_shape_x = read_datasets.read_data(path)
    # Split into train/test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42)

    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

    nb = Pipeline([('vect', CountVectorizer()),
                   ('tfidf', TfidfTransformer()),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(X_train, y_train)

    # % % time
    from sklearn.metrics import classification_report
    y_pred = nb.predict(X_test)

    print('accuracy %s' % accuracy_score(y_pred, y_test))
    my_tags = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    print(classification_report(y_test, y_pred, target_names=my_tags))
