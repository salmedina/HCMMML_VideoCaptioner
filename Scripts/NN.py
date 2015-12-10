from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from collections import namedtuple

layer = namedtuple('layer',['output_dim', 'input_dim', 'init', 'activation', 'dropout'])
sgd_params = namedtuple('sgd_params',['lr', 'decay', 'momentum', 'nesterov'])

class MLP:
    '''
    [(output_dim, input_dim, init, activation, dropout)]
    '''
    def __init__(self\
                 , structure\
                 , sgd_params_init = sgd_params(0.1,1e-6,0.9,True)\
                 , loss_name = 'mean_squared_error'):
        
        self.model = Sequential()
        for layers in structure:
            self.model.add(Dense(output_dim = layers.output_dim\
                                 , input_dim = layers.input_dim\
                                 , init = layers.init\
                                 , activation = layers.activation))
            if layers.dropout != None:
                self.model.add(Dropout(layers.dropout))
                sgd = SGD(lr = sgd_params_init.lr\
                          , decay = sgd_params_init.decay\
                          , momentum = sgd_params_init.momentum\
                          , nesterov = sgd_params_init.nesterov)

        self.model.compile(loss = loss_name, optimizer = sgd)

    def train(self, X_train, y_train, nb_epoch = 20, batch_size = 16):
        self.model.fit(X_train, y_train, nb.epoch, batch_size)    

    def test(self, X_test, y_test, batch_size = 16):
        return self.model.evaluate(X_test, y_test, batch_size)   
