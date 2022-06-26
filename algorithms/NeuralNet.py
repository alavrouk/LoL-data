import time

from keras import Sequential
from keras.layers import Dense
import tensorflow as tf

from util.DataTransformations import neuralNetTransform


def runNeuralNetwork(data, logger):
    """
    Builds a neural network and evaluates it on the data provided in util.neuralNetTransform
    WIP, as we collect more data (more games played in the split), then the network will most
    likely expand and start performing better. But for now, its pretty simple and doesnt really
    perform that well

    :param data: The data generated from dataGenerator.py
    :param logger: The logger created in ChampionsQueueModel.py
    :return: Nothing
    """
    logger.info("Starting Neural Network Operations")

    logger.info("Splitting data into training and validation set")
    d0 = time.perf_counter()
    neuralNetworkData = neuralNetTransform(data, logger)
    toSplit = (int)(neuralNetworkData.shape[0] / (10/8))
    Xtrain = neuralNetworkData[0:toSplit, 1:]
    Ytrain = neuralNetworkData[0:toSplit, 0].reshape((toSplit))
    Xtest = neuralNetworkData[toSplit:neuralNetworkData.shape[0], 1:]
    Ytest = neuralNetworkData[toSplit:neuralNetworkData.shape[0], 0].reshape(
        (neuralNetworkData.shape[0] - toSplit))
    d1 = time.perf_counter()
    logger.info(f"Done in {d1 - d0:0.4f} seconds")

    logger.info("Building and compiling model")
    d0 = time.perf_counter()
    model = Sequential()
    model.add(Dense(20, input_dim=20, activation='relu'))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(15, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    Kevin = tf.keras.optimizers.Adam(
        learning_rate=5e-3,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-07,
        amsgrad=False,
        name='Adam',
    )
    model.compile(optimizer=Kevin,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    d1 = time.perf_counter()
    logger.info(f"Done in {d1 - d0:0.4f} seconds")

    logger.info("Fitting and Evaluating Performance")
    d0 = time.perf_counter()
    model.fit(Xtrain, Ytrain, epochs=100, batch_size=10)
    test_loss, test_acc = model.evaluate(Xtest, Ytest)
    d1 = time.perf_counter()
    logger.info(f"Done in {d1 - d0:0.4f} seconds")
    # This is to debug, see predictions on individual datapoints
    Ypreds = model.predict(Xtest)
    for i in range(Xtest.shape[0]):
        print("Predicted: ", Ypreds[i])
        print("Actual: ", Ytest[i])
        print("--------------------------------------------------")
    print("test_loss:", test_loss)
    print("test_acc:", test_acc)

    logger.info("All Neural Network operations complete")
