from NN import MLP, layer, sgd_params
import pdb

'''
layer = namedtuple('layer',['output_dim', 'input_dim', 'init', 'activation', 'dropout'])
sgd_params = namedtuple('sgd_params',['lr', 'decay', 'momentum', 'nesterov'])

'''

if __name__ == "__main__":
    ## create the structure of a NN
    structure = [\
                 layer(64,4096,'uniform','tanh',0.5)\
                 , layer(64,64,'uniform','tanh',0.5)\
                 , layer(4,5,'uniform','softmax',None)\
                 ]
    sgd_params_init = sgd_params(0.1,1e-6,0.9,True)
    loss_name = 'mean_squared_error'

    classifier = MLP(structure,sgd_params_init,loss_name)

    
    # path2pickle = ''
    # X, y = getData(path2pickle)
    # X_train, y_train, X_test, y_test = splitData(X,y)
